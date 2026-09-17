"""
Automated Test Suite for Executive Productivity Agent — AIONOS

Validates all 7 required assignment test cases, hallucination safeguards,
deduplication invariants, and calendar intelligence.
"""

import pytest
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.db import init_db, save_actions, save_calendar_events, get_actions, get_calendar_events
from backend.agents.pipeline import ExecutivePipeline
from backend.services.qa_service import QAAgent
from backend.models.schemas import OwnershipType, ActionStatus

@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    init_db()
    pipeline = ExecutivePipeline(target_date="2026-09-23")
    actions, cal_events, brief = pipeline.run_full_pipeline()
    save_actions(actions)
    save_calendar_events(cal_events)
    return {"actions": actions, "calendar": cal_events, "brief": brief}

# TEST 1: What did I promise Raghav?
def test_case_1_promise_raghav():
    qa = QAAgent()
    res = qa.answer_question("What did I promise Raghav?")
    assert "vendor list" in res.answer.lower(), "Should identify updated vendor list commitment"
    assert "raghav" in res.answer.lower()
    assert res.grounded is True
    assert len(res.sources) >= 2, "Must cite multiple grounded sources"
    assert any("meet_leadership_sync" in s.source_id for s in res.sources), "Must cite Leadership Sync"
    assert any("vendor_list" in s.source_id for s in res.sources), "Must cite Vendor List email"

# TEST 2: What needs action today?
def test_case_2_action_today():
    qa = QAAgent()
    res = qa.answer_question("What needs action today?")
    assert res.grounded is True
    assert "vendor list" in res.answer.lower(), "Should include vendor list (due/overdue today)"
    assert "meridian" in res.answer.lower(), "Should include Meridian Logistics sync"
    assert "act_vendor_list" in res.related_action_ids
    assert "act_meridian_sync" in res.related_action_ids

# TEST 3: Who owns the Mumbai lease?
def test_case_3_mumbai_lease_unclear_ownership():
    qa = QAAgent()
    res = qa.answer_question("Who owns the Mumbai lease?")
    assert "unclear" in res.answer.lower(), "Must explicitly declare ownership is unclear"
    assert "no owner has been confirmed" in res.answer.lower() or "unassigned and unowned" in res.answer.lower()
    assert "act_mumbai_lease" in res.related_action_ids
    
    actions = get_actions()
    lease_action = next((a for a in actions if a.id == "act_mumbai_lease"), None)
    assert lease_action is not None
    assert lease_action.ownership_status == OwnershipType.UNCLEAR, "Must NOT be assigned to Arjun"
    assert lease_action.owner == "Unclear"

# TEST 4: Is the expense report still pending?
def test_case_4_expense_report_completed():
    qa = QAAgent()
    res = qa.answer_question("Is the expense report still pending?")
    assert "no" in res.answer.lower()
    assert "completed" in res.answer.lower()
    assert "divya" in res.answer.lower()
    assert "act_expense_report" in res.related_action_ids
    
    actions = get_actions()
    exp_action = next((a for a in actions if a.id == "act_expense_report"), None)
    assert exp_action is not None
    assert exp_action.status == ActionStatus.COMPLETED, "Status must be COMPLETED based on Wednesday delivery"

# TEST 5: When is the campaign deck review?
def test_case_5_campaign_deck_review_time():
    qa = QAAgent()
    res = qa.answer_question("When is the campaign deck review?")
    assert "thursday" in res.answer.lower()
    assert "9:30" in res.answer or "09:30" in res.answer
    assert "conflict" in res.answer.lower(), "Must surface calendar clash with Board Prep"

# TEST 6: What happened to the Meridian call?
def test_case_6_meridian_call_rescheduled():
    qa = QAAgent()
    res = qa.answer_question("What happened to the Meridian call?")
    assert "rescheduled" in res.answer.lower() or "moved" in res.answer.lower()
    assert "wednesday" in res.answer.lower()
    assert "3:00" in res.answer or "15:00" in res.answer
    assert "priya" in res.answer.lower()

# TEST 7: Show duplicate commitments (Deduplication)
def test_case_7_cross_source_deduplication():
    qa = QAAgent()
    res = qa.answer_question("Show duplicate commitments.")
    assert "vendor list" in res.answer.lower()
    assert "deduplication" in res.answer.lower() or "consolidated" in res.answer.lower()
    
    actions = get_actions()
    vl_actions = [a for a in actions if "vendor list" in a.action.lower()]
    assert len(vl_actions) == 1, "Must show exactly 1 consolidated action, not 3 separate actions"
    assert vl_actions[0].deduplication_count == 3, "Deduplication count should record 3 sources"
    assert len(vl_actions[0].sources) == 3, "Must retain 3 source references"

# Rule 7 Safety: Unanswerable query fallback
def test_rule_7_hallucination_safeguard():
    qa = QAAgent()
    res = qa.answer_question("What is the company budget for 2028?")
    assert res.answer == "I don't have enough evidence in the provided sources to answer that."
    assert res.grounded is False

# Calendar Conflict Detection Test
def test_calendar_conflict_detection():
    events = get_calendar_events(user_key="arjun")
    thursday_events = [e for e in events if e.date == "2026-09-24"]
    conflicts = [e for e in thursday_events if e.has_conflict]
    assert len(conflicts) == 2, "Both Board Prep and Campaign Deck Review must be flagged with conflict"
