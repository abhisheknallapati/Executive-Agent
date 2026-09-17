# Executive Productivity Agent — AIONOS

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Pytest](https://img.shields.io/badge/pytest-9.1+-green.svg)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An enterprise-grade, autonomous executive productivity agent designed for **Arjun Malhotra — VP Sales, Veridian Corp** (`arjun.malhotra@veridian-corp.example`).

The system ingests noisy, multi-modal enterprise communication streams—including **meeting transcripts, email threads, calendar invites, and voice notes**—for the week of **Monday, 21 September 2026 to Friday, 25 September 2026**. It transforms them into a grounded, high-signal daily action brief featuring cross-source deduplication, strict ownership boundaries, conflict resolution, calendar intelligence, and defensible source traceability.

---

## 🌟 Key Features

1. **Personal Commitment Extraction**: Accurately separates commitments made by Arjun (*"My Actions"*) from deliverables owned by colleagues (*"Waiting On Others"*). For example, Divya's financial variance report never becomes an Arjun action.
2. **Semantic Cross-Source Deduplication**: Identifies identical commitments across multiple modalities (e.g. Vendor list appearing in Leadership Sync, Email Thread, and Voice Note 1) and consolidates them into **1 unified action card** while preserving all underlying source links (66% clutter reduction).
3. **Strict Ownership Defense (Rule 1)**: For items with unconfirmed responsibility (e.g. the Mumbai Office Lease Renewal agreement due Friday), the agent **refuses to guess** and explicitly flags it as `⚠️ UNCLEAR OWNERSHIP`.
4. **Temporal Conflict Resolution**: Automatically resolves shifting deadlines using timestamp precedence. When Neha moves the campaign deck review from Wednesday afternoon to Thursday morning, the agent updates the target date to **Thursday, 24 September at 9:30 AM**.
5. **Verified Status Engine (Rule 3)**: Actions are never marked completed without explicit receipt proof. Divya's Expense Variance Report was delivered Wednesday at 5:45 PM and acknowledged at 6:15 PM, shifting its status to `COMPLETED` and removing it from open waiting items.
6. **Calendar Intelligence & Conflict Detection**: Identifies scheduling double-bookings without silently mutating invites (e.g., surfaces a 30-minute clash on Thursday morning between Board Prep and Campaign Deck Review).
7. **Grounded Q&A with Verbatim Citations**: A conversational agent strictly governed by Hallucination Safeguards (Rules 1–7), returning direct quotes and refusing out-of-scope queries (Rule 7).
8. **Audit Trail & Explainability Drawer**: Every badge, status, and deadline links to an audit drawer explaining *Why this action exists*, *What evidence supports it*, and *Direct source quotes*.

---

## 🏛️ System Architecture

```
                               MULTI-MODAL INPUT STREAM
               [Leadership Sync]   [5 Email Threads]   [2 Voice Notes]   [4 Calendars]
                                            │
                                            ▼
                                1. Ingestion Agent
                                            │
                                            ▼
                           2. Source Normalization Agent
                           (Anchors to 21-25 Sep 2026 week)
                                            │
                                            ▼
                          3. Commitment Extraction Agent
                                            │
                                            ▼
                           4. Deadline & Ownership Agent
                           (Enforces Rule 1 & Rule 2)
                                            │
                                            ▼
                           5. Deduplication Agent
                           (Consolidates across modalities)
                                            │
                                            ▼
                        6. Conflict & Status Resolution
                           (Latest explicit statement wins)
                                            │
                                            ▼
                           7. Calendar Intelligence
                           (Detects 30-min schedule clashes)
                                            │
                                            ▼
                        8. SQLite State & Action Database
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
         9. Daily Brief Generator                       10. Grounded Q&A Agent
    (KPIs, Priority Panel, Risks)                     (Source-backed chat + Rule 7)
```

---

## 🚀 Quickstart & Demo Instructions

### Option 1: Zero-Dependency Single Command (Recommended)
This runs the FastAPI server and serves the full executive single-page dashboard at `http://localhost:8000`:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the executive agent
python run.py
```

Open your browser at **`http://localhost:8000`**.

### Option 2: Docker / Docker Compose
```bash
docker-compose up --build
```
Access the application at `http://localhost:8000`.

### Option 3: Standard React + Vite Frontend Workflow
If you prefer running the separate Vite development server:
```bash
# Terminal 1: Backend
python run.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

---

## 🧪 Automated Test Suite (All 7 Benchmarks Passed)

Run the full automated test suite using `pytest`:

```bash
python -m pytest tests/test_agent.py -v
```

### Verified Test Matrix:
| Test ID | Benchmark Scenario | Expected Output | Status |
| :--- | :--- | :--- | :---: |
| **TEST 1** | *"What did I promise Raghav?"* | Updated vendor list; cites 3 sources (Sync, Email, Voice Note); flags overdue. | **PASS** |
| **TEST 2** | *"What needs action today?"* | Surfaced Arjun's Wednesday commitments: Vendor list (overdue) and Meridian sync (3 PM). | **PASS** |
| **TEST 3** | *"Who owns the Mumbai lease?"* | Explicitly marks `⚠️ UNCLEAR OWNERSHIP`; refuses to assign to Arjun per Rule 1. | **PASS** |
| **TEST 4** | *"Is the expense report still pending?"* | Confirms `COMPLETED` (delivered Wed 5:45 PM, acknowledged by Arjun at 6:15 PM). | **PASS** |
| **TEST 5** | *"When is the campaign deck review?"* | Thursday 24 Sep at 9:30 AM (rescheduled from Wed); flags calendar clash with Board Prep. | **PASS** |
| **TEST 6** | *"What happened to the Meridian call?"* | Moved from Monday to Wednesday 23 Sep at 3:00 PM and confirmed per Priya Nair's email. | **PASS** |
| **TEST 7** | *"Show duplicate commitments."* | Demonstrates 3-source consolidation for vendor list across Meeting, Email, and Voice Note. | **PASS** |
| **SAFETY** | *"What is the company budget for 2028?"* | Standard Rule 7 refusal: *"I don't have enough evidence in the provided sources to answer that."* | **PASS** |
| **CALENDAR**| *Schedule Overlap Evaluation* | Correctly flags 30-min clash between Board Prep and Campaign Deck Review on Thursday. | **PASS** |

---

## 📂 Project Structure

```
executive-productivity-agent/
├── backend/
│   ├── agents/
│   │   └── pipeline.py          # 10-stage processing pipeline
│   ├── models/
│   │   └── schemas.py           # Pydantic schemas (ActionItem, SourceReference, Brief)
│   ├── services/
│   │   ├── db.py                # SQLite abstraction layer
│   │   └── qa_service.py        # Grounded Q&A agent enforcing Rules 1-7
│   ├── static/
│   │   └── index.html           # Modern responsive Executive Dashboard SPA
│   └── main.py                  # FastAPI application entrypoint
├── data/
│   ├── seed_data.py             # Verbatim canonical assignment dataset
│   └── seed_data.json           # JSON export of raw inputs
├── docs/
│   ├── DEMO_SCRIPT.md           # 15-minute minute-by-minute defense guide
│   ├── ARCHITECTURE.md          # In-depth architectural technical specification
│   ├── ASSUMPTIONS.md           # Business constraints and calendar boundaries
│   └── AI_TOOLS.md              # AI vs deterministic reasoning inventory
├── frontend/                    # Vite + React + Tailwind project structure
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
├── ppt/
│   ├── generate_ppt.py          # Programmatic PPTX generation script
│   └── Executive_Productivity_Agent_AIONOS.pptx # 10-Slide presentation deck
├── tests/
│   └── test_agent.py            # Pytest test suite covering all 7 scenarios
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py                       # Single-command launcher
└── README.md
```

---

## 📊 Presentation & Demo Script

- **10-Slide PowerPoint Presentation**: Located at `ppt/Executive_Productivity_Agent_AIONOS.pptx`. Strictly structured into 10 widescreen executive slides covering Problem, Solution, Sources, Architecture, Commitment Intelligence, Deduplication & Ownership, Dashboard, Test Cases, and Tech Stack.
- **15-Minute Defense Guide**: Located at `docs/DEMO_SCRIPT.md`. Provides word-for-word talking points, click paths, and Q&A strategies broken down minute-by-minute from `0:00` to `15:00`.

---

## 🛡️ Hallucination Safeguards (Rules 1–7)

1. **Rule 1 (Never invent an owner)**: Unconfirmed commitments (Mumbai lease) remain `UNCLEAR`.
2. **Rule 2 (Never invent a deadline)**: Relative dates are resolved strictly against 21–25 September 2026.
3. **Rule 3 (Never mark completed without evidence)**: Requires explicit delivery receipts.
4. **Rule 4 (Latest explicit evidence wins)**: Temporal precedence resolves shifting schedules.
5. **Rule 5 (Surface unresolved conflicts)**: Flag schedule clashes and disputed ownership.
6. **Rule 6 (Verbatim evidence)**: Every card and answer includes clickable source citations.
7. **Rule 7 (Refuse without evidence)**: Unknown queries return a standard polite refusal.

---

## 📜 License
MIT License. Built for the AIONOS Technical Assignment.
