"""Customer chat endpoint — primary path for n8n testing."""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.lead import Lead
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import ChatRequest, ChatResponse, MessageOut, LeadOut
from app.services.n8n_client import trigger_message_processing

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(body: ChatRequest, db: Session = Depends(get_db)):
    """
    Customer sends a message.

    Flow:
    1. Create or reuse Lead + Conversation
    2. Store customer message
    3. Trigger n8n webhook (PRH-LEAD-PROCESS-MESSAGE)
    4. Return immediately (bot reply arrives via n8n callback or polling)
    """
    # --- Lead ---
    lead: Lead | None = None
    if body.lead_id:
        lead = db.get(Lead, body.lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
    else:
        lead = Lead(
            name=body.name,
            email=body.email,
            phone=body.phone,
            source="WEB_CHAT",
            status="NEW",
        )
        db.add(lead)
        db.flush()

    # Update contact if provided later
    if body.name and not lead.name:
        lead.name = body.name
    if body.email and not lead.email:
        lead.email = body.email
    if body.phone and not lead.phone:
        lead.phone = body.phone

    # --- Conversation ---
    conversation: Conversation | None = None
    if body.conversation_id:
        conversation = db.get(Conversation, body.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(lead_id=lead.id, channel="WEB", status="ACTIVE")
        db.add(conversation)
        db.flush()

    # --- Customer message ---
    customer_msg = Message(
        conversation_id=conversation.id,
        sender_type="CUSTOMER",
        content=body.content.strip(),
        status="RECEIVED",
    )
    db.add(customer_msg)
    db.commit()
    db.refresh(customer_msg)
    db.refresh(lead)
    db.refresh(conversation)

    # --- Trigger n8n ---
    event = {
        "event": "MESSAGE_RECEIVED",
        "message_id": customer_msg.id,
        "conversation_id": conversation.id,
        "lead_id": lead.id,
        "content": customer_msg.content,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "lead": {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "intent": lead.intent,
            "property_type": lead.property_type,
            "bedrooms": lead.bedrooms,
            "location": lead.location,
            "budget_max": lead.budget_max,
            "timeline": lead.timeline,
            "score": lead.score,
            "classification": lead.classification,
        },
    }

    customer_msg.status = "PROCESSING"
    db.commit()

    triggered = await trigger_message_processing(event)
    if not triggered:
        # Fallback bot reply so the UI still works while testing without n8n
        fallback = Message(
            conversation_id=conversation.id,
            sender_type="BOT",
            content=(
                "Thanks for your message! I've received your enquiry. "
                "Our team will review it shortly. "
                "(n8n workflow is not connected yet — configure the webhook to enable AI replies.)"
            ),
            status="PROCESSED",
        )
        db.add(fallback)
        customer_msg.status = "PROCESSED"
        db.commit()
        db.refresh(fallback)

        return ChatResponse(
            conversation_id=conversation.id,
            lead_id=lead.id,
            customer_message=MessageOut.model_validate(customer_msg),
            bot_message=MessageOut.model_validate(fallback),
            lead=LeadOut.model_validate(lead),
            processing=False,
        )

    return ChatResponse(
        conversation_id=conversation.id,
        lead_id=lead.id,
        customer_message=MessageOut.model_validate(customer_msg),
        bot_message=None,
        lead=LeadOut.model_validate(lead),
        processing=True,
    )


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageOut])
def list_messages(conversation_id: str, db: Session = Depends(get_db)):
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return [MessageOut.model_validate(m) for m in conversation.messages]


@router.get("/leads/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: str, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadOut.model_validate(lead)
