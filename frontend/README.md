# Frontend — React

Customer chat interface and sales dashboard for the Real Estate Lead Bot.

## Responsibilities

- Customer chat UI
- Lead forms
- Sales dashboard
- Lead lists & details
- Conversation display
- Follow-up interface
- Loading / error / empty states

## Structure

```text
frontend/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   ├── chat/
│   │   ├── leads/
│   │   ├── dashboard/
│   │   └── followups/
│   ├── pages/
│   │   ├── customer/
│   │   ├── auth/
│   │   └── dashboard/
│   ├── services/
│   ├── hooks/
│   ├── types/
│   ├── utils/
│   └── app/
├── package.json
└── README.md
```

## Local Development

```bash
cd frontend
npm install
npm run dev
```

The app will typically run on `http://localhost:5173` (Vite) or `http://localhost:3000`.

## Important Rules

- Do **not** put business rules or lead scoring in the frontend.
- Do **not** connect directly to PostgreSQL.
- All data access goes through the FastAPI backend.
