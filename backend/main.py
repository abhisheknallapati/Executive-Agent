"""
FastAPI Application for Executive Productivity Agent — AIONOS
"""

import os
from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.models.schemas import ActionItem, CalendarEvent, DailyBrief, QAResponse
from backend.services.db import init_db, save_actions, save_calendar_events, get_actions, get_action_by_id, get_calendar_events
from backend.agents.pipeline import ExecutivePipeline
from backend.services.qa_service import QAAgent
from data.seed_data import MEETING_TRANSCRIPTS, EMAIL_THREADS, VOICE_NOTES, CALENDARS, PEOPLE

app = FastAPI(
    title="Executive Productivity Agent — AIONOS",
    description="Intelligent multi-stage pipeline converting executive inputs into high-signal action briefs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = ExecutivePipeline()
qa_agent = QAAgent()

@app.on_event("startup")
def startup_event():
    init_db()
    actions, cal_events, _ = pipeline.run_full_pipeline()
    save_actions(actions)
    save_calendar_events(cal_events)
    print(f"Server initialized with {len(actions)} actions and {len(cal_events)} calendar events.")

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "agent_user": "Arjun Malhotra — VP Sales",
        "reference_week": "21–25 September 2026",
        "system": "AIONOS Executive Productivity Agent"
    }

@app.get("/api/brief", response_model=DailyBrief)
def get_daily_brief(date: str = "2026-09-23"):
    p = ExecutivePipeline(target_date=date)
    actions, cal_events, brief = p.run_full_pipeline()
    save_actions(actions)
    save_calendar_events(cal_events)
    return brief

@app.get("/api/actions", response_model=List[ActionItem])
def list_actions(
    ownership_status: Optional[str] = Query(None, description="ARJUN, OTHER, UNCLEAR"),
    status: Optional[str] = Query(None, description="DUE_TODAY, OVERDUE, UPCOMING, COMPLETED, UNCLEAR")
):
    return get_actions(ownership_status=ownership_status, status=status)

@app.get("/api/actions/{action_id}", response_model=ActionItem)
def get_action_detail(action_id: str):
    item = get_action_by_id(action_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action not found")
    return item

@app.get("/api/calendar", response_model=List[CalendarEvent])
def list_calendar(date: Optional[str] = None):
    return get_calendar_events(date=date, user_key="arjun")

@app.get("/api/sources")
def get_all_sources():
    return {
        "people": PEOPLE,
        "meeting_transcripts": MEETING_TRANSCRIPTS,
        "email_threads": EMAIL_THREADS,
        "voice_notes": VOICE_NOTES,
        "calendars": CALENDARS
    }

class ChatQuery(BaseModel):
    query: str

@app.post("/api/chat", response_model=QAResponse)
def chat_with_agent(payload: ChatQuery):
    return qa_agent.answer_question(payload.query)

@app.post("/api/pipeline/run")
def trigger_pipeline(target_date: str = "2026-09-23"):
    p = ExecutivePipeline(target_date=target_date)
    actions, cal_events, brief = p.run_full_pipeline()
    save_actions(actions)
    save_calendar_events(cal_events)
    return {
        "message": "Pipeline executed successfully",
        "audit_log": [step.model_dump() for step in p.audit_log],
        "kpis": brief.kpis
    }

# Mount static files for the single-page application dashboard
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "message": "Executive Productivity Agent API is running. Build static UI in backend/static/index.html."
    }
