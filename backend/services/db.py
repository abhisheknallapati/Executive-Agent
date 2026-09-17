import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from backend.models.schemas import ActionItem, CalendarEvent, OwnershipType, ActionStatus, SourceReference, SourceType

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "executive_agent.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actions (
        id TEXT PRIMARY KEY,
        action TEXT NOT NULL,
        owner TEXT NOT NULL,
        ownership_status TEXT NOT NULL,
        stakeholder TEXT NOT NULL,
        deadline TEXT NOT NULL,
        normalized_deadline TEXT,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        confidence TEXT NOT NULL,
        sources_json TEXT NOT NULL,
        evidence_json TEXT NOT NULL,
        latest_evidence TEXT NOT NULL,
        why_exists TEXT NOT NULL,
        conflict_note TEXT,
        last_updated TEXT NOT NULL,
        deduplication_count INTEGER DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calendar_events (
        id TEXT PRIMARY KEY,
        user_key TEXT NOT NULL,
        title TEXT NOT NULL,
        day TEXT NOT NULL,
        date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        attendees_json TEXT NOT NULL,
        location TEXT,
        notes TEXT,
        has_conflict INTEGER DEFAULT 0,
        conflict_reason TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        step_number INTEGER NOT NULL,
        step_name TEXT NOT NULL,
        agent_name TEXT NOT NULL,
        description TEXT NOT NULL,
        details_json TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def save_actions(actions: List[ActionItem]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM actions;")
    
    for item in actions:
        sources_data = [s.model_dump() for s in item.sources]
        cursor.execute("""
            INSERT INTO actions (
                id, action, owner, ownership_status, stakeholder, deadline,
                normalized_deadline, status, priority, confidence,
                sources_json, evidence_json, latest_evidence, why_exists,
                conflict_note, last_updated, deduplication_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.id,
            item.action,
            item.owner,
            item.ownership_status.value,
            item.stakeholder,
            item.deadline,
            item.normalized_deadline,
            item.status.value,
            item.priority,
            item.confidence,
            json.dumps(sources_data),
            json.dumps(item.evidence),
            item.latest_evidence,
            item.why_exists,
            item.conflict_note,
            item.last_updated,
            item.deduplication_count
        ))
    conn.commit()
    conn.close()

def get_actions(ownership_status: Optional[str] = None, status: Optional[str] = None) -> List[ActionItem]:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM actions WHERE 1=1"
    params = []
    if ownership_status:
        query += " AND ownership_status = ?"
        params.append(ownership_status)
    if status:
        query += " AND status = ?"
        params.append(status)
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    actions = []
    for r in rows:
        sources_list = [SourceReference(**s) for s in json.loads(r["sources_json"])]
        actions.append(ActionItem(
            id=r["id"],
            action=r["action"],
            owner=r["owner"],
            ownership_status=OwnershipType(r["ownership_status"]),
            stakeholder=r["stakeholder"],
            deadline=r["deadline"],
            normalized_deadline=r["normalized_deadline"],
            status=ActionStatus(r["status"]),
            priority=r["priority"],
            confidence=r["confidence"],
            sources=sources_list,
            evidence=json.loads(r["evidence_json"]),
            latest_evidence=r["latest_evidence"],
            why_exists=r["why_exists"],
            conflict_note=r["conflict_note"],
            last_updated=r["last_updated"],
            deduplication_count=r["deduplication_count"]
        ))
    conn.close()
    return actions

def get_action_by_id(action_id: str) -> Optional[ActionItem]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM actions WHERE id = ?", (action_id,))
    r = cursor.fetchone()
    conn.close()
    if not r:
        return None
    sources_list = [SourceReference(**s) for s in json.loads(r["sources_json"])]
    return ActionItem(
        id=r["id"],
        action=r["action"],
        owner=r["owner"],
        ownership_status=OwnershipType(r["ownership_status"]),
        stakeholder=r["stakeholder"],
        deadline=r["deadline"],
        normalized_deadline=r["normalized_deadline"],
        status=ActionStatus(r["status"]),
        priority=r["priority"],
        confidence=r["confidence"],
        sources=sources_list,
        evidence=json.loads(r["evidence_json"]),
        latest_evidence=r["latest_evidence"],
        why_exists=r["why_exists"],
        conflict_note=r["conflict_note"],
        last_updated=r["last_updated"],
        deduplication_count=r["deduplication_count"]
    )

def save_calendar_events(events: List[CalendarEvent], user_key: str = "arjun"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calendar_events WHERE user_key = ?", (user_key,))
    for ev in events:
        cursor.execute("""
            INSERT INTO calendar_events (
                id, user_key, title, day, date, start_time, end_time,
                attendees_json, location, notes, has_conflict, conflict_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ev.id,
            user_key,
            ev.title,
            ev.day,
            ev.date,
            ev.start_time,
            ev.end_time,
            json.dumps(ev.attendees),
            ev.location,
            ev.notes,
            1 if ev.has_conflict else 0,
            ev.conflict_reason
        ))
    conn.commit()
    conn.close()

def get_calendar_events(date: Optional[str] = None, user_key: str = "arjun") -> List[CalendarEvent]:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM calendar_events WHERE user_key = ?"
    params = [user_key]
    if date:
        query += " AND date = ?"
        params.append(date)
    query += " ORDER BY start_time ASC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    events = []
    for r in rows:
        events.append(CalendarEvent(
            id=r["id"],
            title=r["title"],
            day=r["day"],
            date=r["date"],
            start_time=r["start_time"],
            end_time=r["end_time"],
            attendees=json.loads(r["attendees_json"]),
            location=r["location"],
            notes=r["notes"],
            has_conflict=bool(r["has_conflict"]),
            conflict_reason=r["conflict_reason"]
        ))
    conn.close()
    return events
