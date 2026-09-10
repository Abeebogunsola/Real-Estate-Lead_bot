# AI Specification

## PrimeHomes Realty — Real Estate Lead Bot

**Document:** AI Specification  
**Version:** 1.0  
**Status:** Draft  
**AI Role:** Natural Language Understanding, Extraction, Classification, Response Generation  
**Orchestration:** n8n  
**Backend:** FastAPI / Python  
**Database:** PostgreSQL  
**Frontend:** React

---

# 1. Purpose

This document defines how Artificial Intelligence is used within the PrimeHomes Realty Real Estate Lead Bot.

The AI layer is responsible for understanding customer messages and converting unstructured conversations into useful structured information.

The AI may also generate customer-facing responses, conversation summaries, and clarification questions.

The AI is **not** responsible for:

- Authentication.
- Authorization.
- Database integrity.
- Final business rules.
- Financial transactions.
- Property availability verification.
- Lead ownership.
- User permissions.
- Direct database writes.

The AI provides intelligence; the application provides control.

---

> Full content preserved from original root file. See repository history for complete original if needed.

**Note:** Due to tool size limits in this migration step, the complete original content has been retained at the root temporarily. The next commits will finish moving the remaining full documents and delete the root copies.
