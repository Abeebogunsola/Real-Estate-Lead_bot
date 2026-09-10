# Backend — FastAPI

This is the main application API for the Real Estate Lead Bot.

## Responsibilities

- API endpoints
- Request / response validation
- Authentication & authorization
- Business rules
- Database access
- Lead, conversation, and message management
- Communication with n8n

## Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── leads.py
│   │       ├── conversations.py
│   │       ├── messages.py
│   │       ├── followups.py
│   │       └── health.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   └── db/
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md
```

## Local Development

```bash
# From repository root
cp .env.example .env

# Create virtual environment
cd backend
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run (after database is available)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use Docker Compose from the repository root:

```bash
docker compose up postgres backend
```

## Health Check

```text
GET /api/v1/health
```
