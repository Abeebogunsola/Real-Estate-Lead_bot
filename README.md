# REAL ESTATE LEAD BOT

## PrimeHomes Realty

AI-powered real estate lead assistant: chat → FastAPI → **n8n** → MySQL → sales-ready leads.

---

## Stack (current)

| Layer | Tech |
|-------|------|
| Frontend | React + Vite (blue / off-white UI) |
| Backend | FastAPI (Python) |
| Database | **MySQL 8** |
| Automation | **n8n** (Docker) |
| Runtime | Docker Compose |

---

## Quick start (Docker)

### 1. Clone & env

```bash
git clone https://github.com/Abeebogunsola/Real-Estate-Lead_bot.git
cd Real-Estate-Lead_bot

cp .env.example .env
```

### 2. Start everything

```bash
docker compose up --build -d
```

First start may take a minute while MySQL becomes healthy and tables are created.

### 3. Open the apps

| Service | URL |
|---------|-----|
| **Frontend (chat)** | http://localhost:3000 |
| **Backend API docs** | http://localhost:8000/docs |
| **Health** | http://localhost:8000/api/v1/health |
| **n8n** | http://localhost:5678 |

n8n login (default):

- User: `admin`
- Password: `admin`

### 4. Useful commands

```bash
# Logs
docker compose logs -f backend
docker compose logs -f n8n
docker compose logs -f mysql

# Restart one service
docker compose restart backend

# Stop all
docker compose down

# Stop and wipe DB volume
docker compose down -v
```

---

## How the flow works

```text
Customer (React chat)
        ↓
POST /api/v1/chat
        ↓
FastAPI stores Lead + Conversation + Message in MySQL
        ↓
POST → n8n webhook  (lead-process-message)
        ↓
n8n: AI extract → PATCH lead → POST bot-reply
        ↓
Frontend polls messages → shows bot reply + lead score
```

### Backend endpoints for n8n

| Method | Path | Purpose |
|--------|------|--------|
| `POST` | `/api/v1/chat` | Customer message (also used by UI) |
| `GET` | `/api/v1/conversations/{id}/messages` | Poll messages |
| `GET` | `/api/v1/leads/{id}` | Lead details |
| `PATCH` | `/api/v1/internal/leads/{id}` | n8n updates extracted fields |
| `POST` | `/api/v1/internal/leads/{id}/qualify` | Recalculate score |
| `POST` | `/api/v1/internal/bot-reply` | n8n saves bot message |

Inside Docker, n8n must call the backend as **`http://backend:8000`** (not localhost).

---

## Configure n8n workflow

1. Open http://localhost:5678 and log in.
2. Create a workflow with a **Webhook** node:
   - Method: `POST`
   - Path: `lead-process-message`
3. Set env so FastAPI hits that webhook:

   ```env
   N8N_WEBHOOK_URL=http://n8n:5678/webhook/lead-process-message
   ```

   (Already set in `docker-compose.yml` for the backend service.)

4. After AI extraction, add **HTTP Request** nodes:

   **Update lead**

   ```text
   PATCH http://backend:8000/api/v1/internal/leads/{{ $json.lead_id }}
   ```

   Body (example):

   ```json
   {
     "lead_id": "...",
     "intent": "BUY",
     "property_type": "APARTMENT",
     "bedrooms": 3,
     "location": "Lekki",
     "budget_max": 80000000,
     "currency": "NGN",
     "timeline": "WITHIN_3_MONTHS"
   }
   ```

   FastAPI will **recalculate score + classification** automatically.

   **Save bot reply**

   ```text
   POST http://backend:8000/api/v1/internal/bot-reply
   ```

   ```json
   {
     "conversation_id": "...",
     "message_id": "...",
     "content": "Thanks! I noted a 3-bedroom in Lekki around ₦80M. When are you looking to buy?"
   }
   ```

5. Activate the workflow.

More detail: [`n8n/workflows/README.md`](n8n/workflows/README.md).

---

## Test without n8n first

If the n8n webhook is unreachable, the API still returns a **fallback bot message** so you can verify UI + MySQL.

```bash
curl -s http://localhost:8000/api/v1/health | jq

curl -s -X POST http://localhost:8000/api/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"content":"I need a 3-bedroom apartment in Lekki around 80 million"}' | jq
```

---

## Local frontend only (optional)

```bash
cd frontend
npm install
npm run dev
# http://localhost:5173  (proxies /api → localhost:8000)
```

---

## Project layout

```text
backend/          FastAPI + MySQL models + n8n callbacks
frontend/         Modern chat UI (blue / off-white)
n8n/workflows/    Workflow notes for n8n
docs/             Specs & task tracker
docker-compose.yml
```

---

## Docs

See [`docs/README.md`](docs/README.md) for product, architecture, and qualification rules.
