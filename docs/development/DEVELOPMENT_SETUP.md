# Development Setup

> **Note:** Full content is in the original DEVELOPMENT_SETUP.md at the root (during transition).

## Quick Start

```bash
# Clone
git clone https://github.com/Abeebogunsola/Real-Estate-Lead_bot.git
cd Real-Estate-Lead_bot

# Environment
cp .env.example .env

# Start infrastructure
docker compose up -d postgres n8n

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

See the original DEVELOPMENT_SETUP.md for the full recommended development sequence and principles.
