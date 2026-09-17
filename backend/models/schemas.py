from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class OwnershipType(str, Enum):
    ARJUN = "ARJUN"
    OTHER = "OTHER"
    UNCLEAR = "UNCLEAR"

class ActionStatus(str, Enum):
    DUE_TODAY = "DUE_TODAY"
    OVERDUE = "OVERDUE"
    UPCOMING = "UPCOMING"
    COMPLETED = "COMPLETED"
    UNCLEAR = "UNCLEAR"

class SourceType(str, Enum):
    EMAIL = "EMAIL"
    CALENDAR = "CALENDAR"
    MEETING = "MEETING"
    VOICE_NOTE = "VOICE_NOTE"

class SourceReference(BaseModel):
    source_id: str
    source_type: SourceType
    title: str
    date_display: str
    timestamp: Optional[str] = None
    sender_or_speaker: Optional[str] = None
    quote: str
    reference_tag: str

class ActionItem(BaseModel):
    id: str
    action: str
    owner: str
    ownership_status: OwnershipType
    stakeholder: str
    deadline: str
    normalized_deadline: Optional[str] = None
    status: ActionStatus
    priority: str = "Medium"
    confidence: str = "High"
    sources: List[SourceReference] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    latest_evidence: str
    why_exists: str
    conflict_note: Optional[str] = None
    last_updated: str
    deduplication_count: int = 1

class CalendarEvent(BaseModel):
    id: str
    title: str
    day: str
    date: str
    start_time: str
    end_time: str
    attendees: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    notes: Optional[str] = None
    has_conflict: bool = False
    conflict_reason: Optional[str] = None

class KeyRisk(BaseModel):
    id: str
    title: str
    severity: str
    description: str
    owner_status: str
    deadline: str
    action_ref_id: Optional[str] = None

class DailyBrief(BaseModel):
    simulated_date: str
    date_display: str
    greeting: str
    summary: str
    kpis: Dict[str, int]
    needs_action_today: List[ActionItem]
    waiting_on_others: List[ActionItem]
    unclear_ownership: List[ActionItem]
    overdue: List[ActionItem]
    completed: List[ActionItem]
    todays_calendar: List[CalendarEvent]
    calendar_conflicts: List[CalendarEvent]
    key_risks: List[KeyRisk]

class QAResponse(BaseModel):
    question: str
    answer: str
    confidence: str
    sources: List[SourceReference]
    grounded: bool = True
    related_action_ids: List[str] = Field(default_factory=list)
    conflict_notes: Optional[str] = None

class PipelineStepResult(BaseModel):
    step_number: int
    step_name: str
    agent_name: str
    description: str
    status: str = "SUCCESS"
    details: Dict[str, Any]
