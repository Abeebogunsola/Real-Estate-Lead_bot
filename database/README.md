# Database

PostgreSQL is the primary source of truth for the Real Estate Lead Bot.

## Planned Tables

- `users`
- `roles`
- `leads`
- `conversations`
- `messages`
- `lead_scores`
- `lead_assignments`
- `follow_ups`
- `activities`
- `integration_syncs`

## Migrations

Alembic will be used for migrations. Migration files will live under:

```text
backend/alembic/
```

or a dedicated migrations folder once configured.

## Local Development

The easiest way to run PostgreSQL is via Docker Compose from the repository root:

```bash
docker compose up postgres
```

Connection string (matches `.env.example`):

```text
postgresql://postgres:postgres@localhost:5432/real_estate_leads
```

## Important Rules

- PostgreSQL is the system of record.
- Google Sheets is secondary / operational only.
- AI must never write directly to the database.
