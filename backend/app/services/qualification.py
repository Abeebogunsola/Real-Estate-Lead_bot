"""Deterministic lead scoring — does NOT rely on AI for the final score."""

from app.models.lead import Lead


def calculate_score(lead: Lead) -> tuple[int, str]:
    """Return (score 0-100, classification)."""
    score = 0

    # Intent — max 20
    intent = (lead.intent or lead.transaction_type or "").upper()
    if intent in ("BUY", "RENT", "SELL", "LAND"):
        score += 20
    elif intent in ("PROPERTY_ENQUIRY", "GENERAL_ENQUIRY"):
        score += 10

    # Property requirement — max 15
    if lead.property_type:
        score += 10
    if lead.bedrooms is not None and lead.bedrooms > 0:
        score += 5

    # Location — max 15
    if lead.location:
        loc = lead.location.strip().lower()
        if any(x in loc for x in ("lekki", "ikoyi", "victoria island", "vi", "banana island")):
            score += 15
        elif len(loc) > 2:
            score += 8

    # Budget — max 20
    if lead.budget_max is not None or lead.budget_min is not None:
        score += 20
    # (approximate would be +10 — we treat any stated budget as clear for MVP)

    # Timeline — max 20
    timeline = (lead.timeline or "").upper()
    timeline_points = {
        "IMMEDIATE": 20,
        "WITHIN_1_MONTH": 18,
        "WITHIN_3_MONTHS": 15,
        "WITHIN_6_MONTHS": 10,
        "RESEARCHING": 5,
    }
    score += timeline_points.get(timeline, 0)

    # Contact — max 10
    if lead.phone:
        score += 5
    if lead.email:
        score += 3
    if lead.name:
        score += 2

    score = min(100, max(0, score))

    if score >= 80:
        classification = "HOT"
    elif score >= 60:
        classification = "WARM"
    elif score >= 30:
        classification = "COLD"
    else:
        classification = "UNQUALIFIED"

    return score, classification
