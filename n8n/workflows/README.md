# n8n Workflow Setup for Lead Bot

## Quick start (import the sample workflow)

1. Open n8n → http://localhost:5678 (admin / admin)
2. **Workflows** → **Import from File**
3. Select `n8n/workflows/lead-process-message.json` from this repo
4. Open the workflow and click **Active** (toggle ON)
5. The webhook path is already set to `lead-process-message`

That workflow uses a **Code** node for simple rule-based extraction so you can test immediately **without** an OpenAI key. Later you can replace the Code node with an OpenAI / LLM node.

---

## Webhook path

- Method: `POST`
- Path: `lead-process-message`
- From backend (Docker): `http://n8n:5678/webhook/lead-process-message`
- From host browser: `http://localhost:5678/webhook/lead-process-message`

## Incoming payload (from FastAPI)

```json
{
  "event": "MESSAGE_RECEIVED",
  "message_id": "uuid",
  "conversation_id": "uuid",
  "lead_id": "uuid",
  "content": "I need a 3 bedroom in Lekki around 80 million",
  "timestamp": "2026-09-14T12:00:00Z",
  "lead": { "id": "...", "location": null, "score": null }
}
```

## What the sample workflow does

1. **Webhook** receives the payload
2. **Code** node extracts intent / property / bedrooms / location / budget / timeline and drafts a friendly reply
3. **HTTP Request** → `PATCH http://backend:8000/api/v1/internal/leads/{id}`  
   FastAPI recalculates score + classification
4. **HTTP Request** → `POST http://backend:8000/api/v1/internal/bot-reply`  
   Stores the bot message so the frontend can poll it

## Important

- Inside Docker, n8n **must** call the backend as `http://backend:8000` (service name), **not** `localhost`.
- Header `X-Webhook-Secret` must match `N8N_WEBHOOK_SECRET` in `.env` / docker-compose (default: `change-me-n8n-secret`).
- Score and classification are calculated by FastAPI — do not set them from AI.

## Upgrade to real AI later

Replace the **Extract + Draft Reply** Code node with an OpenAI (or other LLM) node that returns structured JSON, then map the fields into the same two HTTP Request nodes.
