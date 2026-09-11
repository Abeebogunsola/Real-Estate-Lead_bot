# n8n Workflow Setup for Lead Bot

## Webhook path

Create a workflow with a **Webhook** trigger:

- Method: `POST`
- Path: `lead-process-message`
- Full URL when running in Docker: `http://n8n:5678/webhook/lead-process-message`
  (from the host browser: `http://localhost:5678/webhook/lead-process-message`)

## Incoming payload (from FastAPI)

```json
{
  "event": "MESSAGE_RECEIVED",
  "message_id": "uuid",
  "conversation_id": "uuid",
  "lead_id": "uuid",
  "content": "I need a 3 bedroom in Lekki",
  "timestamp": "2026-09-11T12:00:00Z",
  "lead": { "id": "...", "location": null, "score": null }
}
```

## Recommended nodes after Webhook

1. **Validate** required fields (`message_id`, `conversation_id`, `lead_id`, `content`)
2. **AI / LLM** node — extract structured JSON (intent, property_type, bedrooms, location, budget_max, timeline, …)
3. **HTTP Request** → update lead:

   `PATCH http://backend:8000/api/v1/internal/leads/{{lead_id}}`

   Body example:

   ```json
   {
     "lead_id": "{{$json.lead_id}}",
     "intent": "BUY",
     "property_type": "APARTMENT",
     "bedrooms": 3,
     "location": "Lekki",
     "budget_max": 80000000,
     "currency": "NGN",
     "timeline": "WITHIN_3_MONTHS"
   }
   ```

   Header (optional): `X-Webhook-Secret: <same as N8N_WEBHOOK_SECRET in .env>`

4. **HTTP Request** → save bot reply:

   `POST http://backend:8000/api/v1/internal/bot-reply`

   ```json
   {
     "conversation_id": "{{$json.conversation_id}}",
     "message_id": "{{$json.message_id}}",
     "content": "Thanks! I noted a 3-bedroom in Lekki around ₦80M. When are you looking to buy?"
   }
   ```

5. (Optional) If classification is HOT, send a notification.

## Important

- Use host `backend` (Docker service name), **not** `localhost`, inside n8n containers.
- Score/classification are calculated by FastAPI when you PATCH the lead — do not invent the official score in AI.
