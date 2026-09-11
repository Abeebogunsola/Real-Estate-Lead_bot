"""Internal endpoints called by n8n (service-to-service)."""

from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import get_db
from app.models.lead import Lead
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.n8n import N8nBotReply, N8nLeadUpdate
from app.schemas.chat import MessageOut, LeadOut
from app.services.qualification import calculate_score

router = APIRouter()


def verify_n8n_secret(x_webhook_secret: str | None = Header(default=None)):
    expected = settings.n8n_webhook_secret
    if expected and expected != "change-me-n8n-secret":
        if x_webhook_secret != expected:
            raise HTTPException(status_code=401, detail="Invalid webhook secret")


@router.post("/internal/bot-reply", response_model=MessageOut)
def save_bot_reply(
    body: N8nBotReply,
    db: Session = Depends(get_db),
    _: None = Depends(verify_n8n_secret),
):
    """n8n calls this after generating a customer-facing response."""
    conversation = db.get(Conversation, body.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    bot_msg = Message(
        conversation_id=conversation.id,
        sender_type="BOT",
        content=body.content.strip(),
        status="PROCESSED",
    )
    db.add(bot_msg)

    # Mark original customer message processed if provided
    if body.message_id:
        original = db.get(Message, body.message_id)
        if original:
            original.status = "PROCESSED"

    db.commit()
    db.refresh(bot_msg)
    return MessageOut.model_validate(bot_msg)


@router.patch("/internal/leads/{lead_id}", response_model=LeadOut)
def update_lead_from_n8n(
    lead_id: str,
    body: N8nLeadUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_n8n_secret),
):
    """n8n pushes extracted fields here. Score is recalculated deterministically."""
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    fields = [
        "intent", "transaction_type", "property_type", "bedrooms",
        "location", "budget_min", "budget_max", "currency", "timeline",
        "name", "email", "phone", "status",
    ]
    for field in fields:
        value = getattr(body, field, None)
        if value is not None:
            setattr(lead, field, value)

    # Deterministic scoring (AI does not set the official score)
    score, classification = calculate_score(lead)
    lead.score = score
    lead.classification = classification
    if lead.status == "NEW":
        lead.status = "QUALIFYING"

    lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(lead)
    return LeadOut.model_validate(lead)


@router.post("/internal/leads/{lead_id}/qualify", response_model=LeadOut)
def qualify_lead(
    lead_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(verify_n8n_secret),
):
    """Force recalculation of score/classification."""
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    score, classification = calculate_score(lead)
    lead.score = score
    lead.classification = classification
    if score >= 30 and lead.status in ("NEW", "QUALIFYING"):
        lead.status = "QUALIFIED"
    lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(lead)
    return LeadOut.model_validate(lead)
