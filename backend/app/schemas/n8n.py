"""Schemas for n8n → FastAPI callbacks."""

from pydantic import BaseModel, Field


class N8nBotReply(BaseModel):
    conversation_id: str
    content: str = Field(..., min_length=1)
    message_id: str | None = None  # original customer message id (optional)


class N8nLeadUpdate(BaseModel):
    lead_id: str
    intent: str | None = None
    transaction_type: str | None = None
    property_type: str | None = None
    bedrooms: int | None = None
    location: str | None = None
    budget_min: float | None = None
    budget_max: float | None = None
    currency: str | None = None
    timeline: str | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    status: str | None = None
    score: int | None = None
    classification: str | None = None
