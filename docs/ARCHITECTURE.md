# System Architecture: Executive Productivity Agent (AIONOS)

## Overview
The Executive Productivity Agent is designed for **Arjun Malhotra (VP Sales, Veridian Corp)** to transform noisy, multi-modal enterprise streams into a verified daily executive action brief with zero hallucination.

```
                    INPUT SOURCES
   [Meeting Transcripts]   [Email Threads]   [Voice Notes]   [Calendars]
                              │
                              ▼
                   1. INGESTION AGENT
               Canonical multi-modal ingestion
                              │
                              ▼
                 2. SOURCE NORMALIZATION AGENT
         Temporal anchoring (21-25 Sep 2026) & ID mapping
                              │
                              ▼
              3. COMMITMENT EXTRACTION AGENT
          Schema extraction of promises & asks
                              │
                              ▼
            4. DEADLINE & OWNERSHIP AGENT
       Rule 1: Strict Ownership (Arjun / Other / Unclear)
       Rule 2: Relative date normalization to ISO
                              │
                              ▼
             5. DEDUPLICATION ENGINE
       Cross-source clustering (Meeting + Email + Voice)
                              │
                              ▼
         6. CONFLICT & STATUS RESOLUTION ENGINE
       Rule 3 & 4: Latest explicit evidence precedence
       Delivery verification (Expense report -> COMPLETED)
                              │
                              ▼
           7. CALENDAR INTELLIGENCE AGENT
       30-min overlap detection (Board Prep vs Deck Review)
                              │
                              ▼
            8. SQLITE ACTION DATABASE & STATE
       Persistent store for actions, citations, audit trail
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    9. DAILY BRIEF GENERATOR        10. GROUNDED Q&A AGENT
   KPIs, Priority Panel, Risks     Interactive chat with Rule 7
```

## Component Directory
- `data/seed_data.py`: Verbatim canonical assignment data for week of 21–25 Sep 2026.
- `backend/models/schemas.py`: Pydantic models for `ActionItem`, `SourceReference`, `CalendarEvent`, `DailyBrief`, `QAResponse`.
- `backend/services/db.py`: SQLite abstraction layer with schema migrations and pre-seeding.
- `backend/agents/pipeline.py`: 10-stage processing pipeline coordinating extraction, deduplication, conflict resolution, and status tracking.
- `backend/services/qa_service.py`: Grounded question-answering agent enforcing Rules 1–7.
- `backend/main.py`: FastAPI server serving REST endpoints and the responsive executive dashboard.
- `backend/static/index.html`: Modern, responsive Single-Page Application with real-time API integrations.
- `tests/test_agent.py`: Pytest automated test suite testing the 7 benchmark scenarios and safety invariants.
- `ppt/generate_ppt.py`: Programmatic generation of the 10-slide executive presentation.
