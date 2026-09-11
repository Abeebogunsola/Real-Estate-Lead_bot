"""Call n8n webhooks. Failures must not break the customer message flow."""

import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def trigger_message_processing(payload: dict[str, Any]) -> bool:
    """Fire-and-forget style call to n8n. Returns True if accepted."""
    url = settings.n8n_webhook_url
    if not url:
        logger.warning("N8N_WEBHOOK_URL not configured — skipping n8n trigger")
        return False

    headers = {"Content-Type": "application/json"}
    if settings.n8n_webhook_secret:
        headers["X-Webhook-Secret"] = settings.n8n_webhook_secret

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code >= 400:
                logger.error("n8n webhook failed: %s %s", resp.status_code, resp.text[:300])
                return False
            logger.info("n8n webhook accepted for message %s", payload.get("message_id"))
            return True
    except Exception as exc:
        logger.exception("n8n webhook error: %s", exc)
        return False
