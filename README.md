# REAL ESTATE LEAD BOT

## PrimeHomes Realty

> An AI-powered real estate lead management system that receives customer enquiries, understands their requirements, qualifies leads, stores customer information, and helps the sales team follow up efficiently.

---

# 1. Project Overview

The **Real Estate Lead Bot** is a digital receptionist and lead qualification system for **PrimeHomes Realty**.

The system is designed to handle incoming customer enquiries automatically instead of requiring a salesperson to manually process every message.

A customer can simply send a message such as:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million."

The system should understand the message, extract the useful information, determine whether additional information is required, qualify the lead, store the information, respond to the customer, and notify the sales team when necessary.

---

# 2. Main Goal

The main goal is to reduce the amount of manual work required to process real estate enquiries.

The system should help PrimeHomes Realty:

- Respond to customers faster.
- Capture leads automatically.
- Reduce forgotten enquiries.
- Extract useful customer information.
- Identify valuable leads.
- Notify sales representatives.
- Maintain conversation history.
- Support follow-up.
- Keep lead information organized.

---

# 3. How the System Works

```text
CUSTOMER
   ↓
REACT CUSTOMER INTERFACE
   ↓
FASTAPI BACKEND
   ↓
N8N WORKFLOW
   ↓
AI PROCESSING
   ↓
LEAD QUALIFICATION
   ↓
POSTGRESQL DATABASE
   ↓
SALES TEAM
   ↓
FOLLOW-UP
```

---

# 4. Technology Stack

| Layer | Technology | Main Responsibility |
|---|---|---|
| Frontend | React | Customer interface and sales dashboard |
| Backend | FastAPI / Python | API and application logic |
| Automation | n8n | Workflow orchestration |
| Database | PostgreSQL | Main source of truth |
| AI | LLM | Understanding and generating responses |
| Reporting | Google Sheets | Operational/reporting projection |
| API Format | REST / JSON | Communication between services |

---

# 5. Project Structure

```text
real-estate-lead-bot/
│
├── frontend/                 # React application
├── backend/                  # FastAPI application
├── n8n/                      # Workflow definitions
├── database/                 # Database notes / seeds
├── tests/                    # Higher-level tests
├── docs/                     # All specifications
│   ├── product/
│   ├── architecture/
│   ├── api/
│   ├── ai/
│   ├── automation/
│   ├── qualification/
│   ├── ui/
│   ├── development/
│   ├── deployment/
│   └── testing/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

# 6. Documentation

All detailed specifications live under [`docs/`](docs/README.md).

Key entry points:

- [Task Tracker](docs/TASK.md)
- [Implementation Log](docs/IMPLEMENTATION.md)
- [Development Setup](docs/development/DEVELOPMENT_SETUP.md)
- [System Architecture](docs/architecture/System-Architecture.md)
- [API Specification](docs/api/API-Specification.md)
- [Lead Qualification](docs/qualification/LEAD_QUALIFICATION_SPEC.md)

---

# 7. Quick Start (Local)

```bash
# 1. Clone & enter
git clone https://github.com/Abeebogunsola/Real-Estate-Lead_bot.git
cd Real-Estate-Lead_bot

# 2. Environment
cp .env.example .env

# 3. Start Postgres + n8n
docker compose up -d postgres n8n

# 4. Backend
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

- Backend: http://localhost:8000  (docs at `/docs`)
- Frontend: http://localhost:5173
- n8n: http://localhost:5678

---

# 8. Development Principles

> **Use the simplest technology that correctly solves the problem.**

- FastAPI owns application/API logic and business boundaries.
- n8n owns automation and integrations.
- AI owns natural-language understanding and generation.
- PostgreSQL is the single source of truth.
- React is the user interface only.

Do not introduce microservices, extra databases, or complex infrastructure unless there is a clear need.

---

# 9. Current Status

| Area | Status |
|------|--------|
| Documentation | 🟢 Complete & reorganized |
| Project scaffolding | 🟢 Complete |
| Backend implementation | ⬜ Skeleton only |
| Frontend implementation | ⬜ Skeleton only |
| Database models | ⬜ Not started |
| n8n workflows | ⬜ Not started |
| AI integration | ⬜ Not started |
| MVP | ⬜ Not yet |

See [docs/TASK.md](docs/TASK.md) and [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) for the detailed tracker.

---

# 10. Agentic Development Rules

When using an AI coding assistant:

1. Read the relevant documentation under `docs/` first.
2. Check `docs/TASK.md` for the current priority.
3. Implement only the scoped task.
4. Run relevant tests.
5. Update `docs/IMPLEMENTATION.md` and `docs/TASK.md`.
6. Do not invent architecture or add unnecessary technologies.

---

# 11. License

See [LICENSE](LICENSE).
