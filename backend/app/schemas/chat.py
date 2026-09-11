"""Chat and lead schemas."""

from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)
    conversation_id: str | None = None
    lead_id: str | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class MessageOut(BaseModel):
    id: str
    conversation_id: str
    sender_type: str
    content: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadOut(BaseModel):
    id: str
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    intent: str | None = None
    transaction_type: str | None = None
    property_type: str | None = None
    bedrooms: int | None = None
    location: str | None = None
    budget_min: float | None = None
    budget_max: float | None = None
    currency: str | None = None
    timeline: str | None = None
    status: str
    score: int | None = None
    classification: str | None = None
    source: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ChatResponse(BaseModel):
    conversation_id: str
    lead_id: str
    customer_message: MessageOut
    bot_message: MessageOut | None = None
    lead: LeadOut | None = None
    processing: bool = True
