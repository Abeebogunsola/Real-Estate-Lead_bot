# n8n Workflows

Automation and workflow orchestration for the Real Estate Lead Bot.

n8n is responsible for:

- Triggering workflows
- Calling AI services
- Processing lead information
- Sending notifications
- Scheduling follow-ups
- Google Sheets synchronization
- Connecting external services

## Principle

> **FastAPI manages the application. n8n manages the workflows.**

## Planned Workflows

| Workflow Name | Purpose |
|---------------|--------|
| `PRH-LEAD-PROCESS-MESSAGE` | Main message processing pipeline |
| `PRH-LEAD-QUALIFY` | Deterministic lead scoring & classification |
| `PRH-LEAD-NOTIFY-SALES` | HOT lead notifications |
| `PRH-FOLLOWUP-REMINDER` | Due follow-up reminders |
| `PRH-SHEET-SYNC-LEAD` | Google Sheets synchronization |
| `PRH-ERROR-HANDLER` | Centralized error handling |

## Folder Structure

```text
n8n/
├── workflows/
│   ├── lead-process-message.json
│   ├── lead-qualify.json
│   ├── lead-notify-sales.json
│   ├── followup-reminder.json
│   ├── sheet-sync-lead.json
│   └── error-handler.json
└── README.md
```

Workflow JSON files will be exported from n8n and stored here for version control.

## Local Access

When running via Docker Compose:

```text
http://localhost:5678
```

Default credentials (change in production):

- User: `admin`
- Password: `admin`
