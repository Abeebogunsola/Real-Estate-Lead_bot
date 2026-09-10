# AI Specification

> **Note:** This document was moved from the repository root.  
> See original "AI Specification.md" for the complete definition.

AI responsibilities:

- Intent detection
- Entity extraction (property type, bedrooms, location, budget, timeline, contact)
- Missing information detection
- Response generation
- Conversation summarization
- Human handoff detection

AI must **not**:

- Write directly to the database
- Own authentication / authorization
- Invent property availability or prices
