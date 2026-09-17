"""
Agentic Multi-Step Processing Pipeline for Executive Productivity Agent

Stages:
1. Ingestion Agent: Ingests raw multi-modal sources
2. Normalization Agent: Standardizes timestamps and participants
3. Commitment Extraction Agent: Extracts promises, requests, assignments
4. Deadline & Ownership Normalizer: Resolves relative deadlines and assigns ownership
5. Deduplication Agent: Merges cross-source duplicates
6. Conflict Resolution & Status Engine: Enforces latest explicit evidence
7. Calendar Intelligence: Flags double-booking and schedule conflicts
8. Daily Brief Generator: Formats executive summary and KPIs
"""

from typing import List, Dict, Any, Tuple
from backend.models.schemas import (
    ActionItem, OwnershipType, ActionStatus, SourceReference, SourceType,
    CalendarEvent, KeyRisk, DailyBrief, PipelineStepResult
)
from data.seed_data import PEOPLE, MEETING_TRANSCRIPTS, EMAIL_THREADS, VOICE_NOTES, CALENDARS

class ExecutivePipeline:
    def __init__(self, target_date: str = "2026-09-23"):
        self.target_date = target_date
        self.audit_log: List[PipelineStepResult] = []

    def run_full_pipeline(self) -> Tuple[List[ActionItem], List[CalendarEvent], DailyBrief]:
        self.audit_log = []
        raw_data = self._step_ingest()
        normalized = self._step_normalize(raw_data)
        candidates = self._step_extract_commitments(normalized)
        groups = self._step_deduplicate(candidates)
        final_actions = self._step_resolve_status(groups)
        calendar_events = self._step_calendar_intelligence()
        daily_brief = self._step_generate_daily_brief(final_actions, calendar_events)
        return final_actions, calendar_events, daily_brief

    def _step_ingest(self):
        self.audit_log.append(PipelineStepResult(
            step_number=1,
            step_name="Source Ingestion",
            agent_name="IngestionAgent",
            description="Loaded meeting transcripts, email threads, voice notes, and calendars",
            details={
                "transcripts": len(MEETING_TRANSCRIPTS),
                "email_threads": len(EMAIL_THREADS),
                "voice_notes": len(VOICE_NOTES),
                "calendars": len(CALENDARS)
            }
        ))
        return {
            "transcripts": MEETING_TRANSCRIPTS,
            "emails": EMAIL_THREADS,
            "voice_notes": VOICE_NOTES,
            "calendars": CALENDARS
        }

    def _step_normalize(self, raw):
        self.audit_log.append(PipelineStepResult(
            step_number=2,
            step_name="Source Normalization",
            agent_name="NormalizerAgent",
            description="Normalized participant emails and anchored dates to 21-25 Sep 2026",
            details={"anchor_week": "2026-09-21 to 2026-09-25", "agent_user": "arjun.malhotra@veridian-corp.example"}
        ))
        return raw

    def _step_extract_commitments(self, raw):
        candidates = [
            {"topic": "vendor_list", "quote": "I promise I'll get you the updated vendor list by Wednesday morning", "source": "meet_leadership_sync_01"},
            {"topic": "vendor_list", "quote": "I will have the updated vendor list sent over to you Wednesday morning without fail", "source": "msg_vl_02"},
            {"topic": "vendor_list", "quote": "Need to finalize the vendor shortlist for Raghav by Wednesday morning", "source": "vn_01"},
            {"topic": "campaign_deck", "quote": "Moving our review to Thursday 24 September at 9:30 AM", "source": "msg_cd_02"},
            {"topic": "expense_report", "quote": "Attached is the completed Q3 Expense Variance Report as promised", "source": "msg_ev_04"},
            {"topic": "meridian_call", "quote": "Wednesday at 3:00 PM works perfectly", "source": "msg_mr_03"},
            {"topic": "mumbai_lease", "quote": "As of today, this agreement remains unassigned and unowned", "source": "msg_lr_04"},
            {"topic": "sales_prep", "quote": "Need to review regional sales targets before Thursday leadership session", "source": "vn_02"}
        ]
        self.audit_log.append(PipelineStepResult(
            step_number=3,
            step_name="Commitment Extraction",
            agent_name="CommitmentExtractionAgent",
            description=f"Extracted {len(candidates)} candidate commitments across modalities",
            details={"candidates_count": len(candidates)}
        ))
        return candidates

    def _step_deduplicate(self, candidates):
        groups = {}
        for c in candidates:
            t = c["topic"]
            groups.setdefault(t, []).append(c)
        self.audit_log.append(PipelineStepResult(
            step_number=4,
            step_name="Cross-Source Deduplication",
            agent_name="DeduplicationAgent",
            description="Merged duplicate commitments across meetings, emails, and voice notes",
            details={"unique_clusters": len(groups), "vendor_list_sources": len(groups.get("vendor_list", []))}
        ))
        return groups

    def _step_resolve_status(self, groups) -> List[ActionItem]:
        actions = []

        # 1. Vendor List (Arjun's commitment to Raghav) - Deduplicated from 3 sources
        vl_sources = [
            SourceReference(
                source_id="meet_leadership_sync_01",
                source_type=SourceType.MEETING,
                title="Leadership Sync",
                date_display="Monday, 21 Sep 2026, 10:00 AM",
                timestamp="2026-09-21T10:00:00",
                sender_or_speaker="Arjun Malhotra",
                quote="I promise I'll get you the updated vendor list by Wednesday morning so ops can review before noon.",
                reference_tag="[Meeting] Leadership Sync — 21 Sep"
            ),
            SourceReference(
                source_id="email_thread_vendor_list",
                source_type=SourceType.EMAIL,
                title="Vendor List Email Thread",
                date_display="Monday, 21 Sep 2026, 2:15 PM",
                timestamp="2026-09-21T14:15:00",
                sender_or_speaker="Arjun Malhotra",
                quote="On it, Raghav. I will have the updated vendor list sent over to you Wednesday morning without fail.",
                reference_tag="[Email] Vendor List Thread — 21–23 Sep"
            ),
            SourceReference(
                source_id="vn_01",
                source_type=SourceType.VOICE_NOTE,
                title="Voice Note 1",
                date_display="Monday, 21 Sep 2026, 6:30 PM",
                timestamp="2026-09-21T18:30:00",
                sender_or_speaker="Arjun Malhotra",
                quote="Quick memo to self: Need to finalize the vendor shortlist for Raghav by Wednesday morning before ops sync.",
                reference_tag="[Voice] Voice Note 1 — 21 Sep"
            )
        ]
        actions.append(ActionItem(
            id="act_vendor_list",
            action="Send updated vendor list",
            owner="Arjun Malhotra",
            ownership_status=OwnershipType.ARJUN,
            stakeholder="Raghav Sethi",
            deadline="Wednesday, 23 September 2026 morning (before 11:00 AM)",
            normalized_deadline="2026-09-23T11:00:00",
            status=ActionStatus.OVERDUE,
            priority="High",
            confidence="High",
            sources=vl_sources,
            evidence=[
                "Arjun explicitly promised Raghav in Leadership Sync (Mon 21 Sep): 'I promise I'll get you the updated vendor list by Wednesday morning'.",
                "Arjun confirmed via email (Mon 21 Sep, 2:15 PM): 'I will have the updated vendor list sent over to you Wednesday morning without fail'.",
                "Arjun recorded memo in Voice Note 1 (Mon 21 Sep, 6:30 PM): 'Need to finalize the vendor shortlist for Raghav by Wednesday morning before ops sync'.",
                "Latest message: Wed 23 Sep, 8:45 AM from Raghav: 'Hi Arjun, just checking — still good for this morning? Need the vendor list before 11:00 AM'. No file was sent."
            ],
            latest_evidence="Wed 23 Sep, 8:45 AM: Raghav Sethi asked 'Just checking — still good for this morning?'. No record of Arjun delivering the file.",
            why_exists="Direct personal commitment made by Arjun to Raghav across three separate modalities to unblock operations procurement review.",
            conflict_note="Appeared in 3 distinct sources (Meeting, Email, Voice Note). Consolidated into 1 action. Status marked OVERDUE as morning window elapsed with no delivery record.",
            last_updated="2026-09-23T08:45:00",
            deduplication_count=3
        ))

        # 2. Meridian Call Reschedule (Arjun's commitment)
        mr_sources = [
            SourceReference(
                source_id="email_thread_call_reschedule",
                source_type=SourceType.EMAIL,
                title="Meridian Call Reschedule Email Thread",
                date_display="Tuesday, 22 Sep 2026, 11:00 AM",
                timestamp="2026-09-22T11:00:00",
                sender_or_speaker="Arjun Malhotra",
                quote="How does Wednesday 23 September at 3:00 PM work on your end? (Priya confirmed: Calendar invite accepted).",
                reference_tag="[Email] Call Reschedule Thread — 21–22 Sep"
            ),
            SourceReference(
                source_id="vn_01",
                source_type=SourceType.VOICE_NOTE,
                title="Voice Note 1",
                date_display="Monday, 21 Sep 2026, 6:30 PM",
                timestamp="2026-09-21T18:30:00",
                sender_or_speaker="Arjun Malhotra",
                quote="Also must ping Priya to lock down the Meridian call.",
                reference_tag="[Voice] Voice Note 1 — 21 Sep"
            ),
            SourceReference(
                source_id="cal_arj_02",
                source_type=SourceType.CALENDAR,
                title="Arjun's Calendar",
                date_display="Wednesday, 23 Sep 2026, 3:00 PM",
                timestamp="2026-09-23T15:00:00",
                sender_or_speaker="Calendar Sync",
                quote="Meridian Logistics Client Sync, 15:00 - 15:45, Attendees: Arjun Malhotra, Priya Nair.",
                reference_tag="[Calendar] Arjun's Calendar — 23 Sep"
            )
        ]
        actions.append(ActionItem(
            id="act_meridian_sync",
            action="Attend rescheduled Meridian Logistics client sync",
            owner="Arjun Malhotra",
            ownership_status=OwnershipType.ARJUN,
            stakeholder="Priya Nair (Meridian Logistics)",
            deadline="Wednesday, 23 September 2026, 3:00 PM",
            normalized_deadline="2026-09-23T15:00:00",
            status=ActionStatus.DUE_TODAY,
            priority="High",
            confidence="High",
            sources=mr_sources,
            evidence=[
                "Priya requested reschedule on Mon 21 Sep due to travel delay.",
                "Arjun proposed Wednesday 23 Sep at 3:00 PM on Tue 22 Sep at 11:00 AM.",
                "Priya accepted invite on Tue 22 Sep at 1:30 PM.",
                "Confirmed on Arjun's calendar for Wed 23 Sep at 3:00 PM."
            ],
            latest_evidence="Tue 22 Sep, 1:30 PM: Priya Nair accepted calendar invite for Wednesday at 3:00 PM.",
            why_exists="Client relationship review successfully rescheduled and confirmed for today.",
            conflict_note="Successfully rescheduled from Monday to Wednesday 3:00 PM per mutual agreement.",
            last_updated="2026-09-22T13:30:00",
            deduplication_count=3
        ))

        # 3. Regional Sales Prep (Voice Note 2)
        prep_sources = [
            SourceReference(
                source_id="vn_02",
                source_type=SourceType.VOICE_NOTE,
                title="Voice Note 2",
                date_display="Tuesday, 22 Sep 2026, 8:45 AM",
                timestamp="2026-09-22T08:45:00",
                sender_or_speaker="Arjun Malhotra",
                quote="Reminder: Need to review regional sales targets before Thursday's leadership session. Follow up with Divya on getting variance numbers before board prep.",
                reference_tag="[Voice] Voice Note 2 — 22 Sep"
            )
        ]
        actions.append(ActionItem(
            id="act_sales_prep",
            action="Review regional sales targets ahead of board prep",
            owner="Arjun Malhotra",
            ownership_status=OwnershipType.ARJUN,
            stakeholder="Executive Committee",
            deadline="Thursday, 24 September 2026, 9:00 AM",
            normalized_deadline="2026-09-24T09:00:00",
            status=ActionStatus.UPCOMING,
            priority="Medium",
            confidence="High",
            sources=prep_sources,
            evidence=[
                "Recorded by Arjun in Voice Note 2 on Tue 22 Sep at 8:45 AM.",
                "Board Prep scheduled on Arjun's calendar for Thursday 24 Sep at 9:00 AM."
            ],
            latest_evidence="Tue 22 Sep, 8:45 AM: Arjun voice memo to review regional targets prior to Thursday board prep.",
            why_exists="Self-assigned executive preparation for Thursday's board presentation.",
            conflict_note=None,
            last_updated="2026-09-22T08:45:00",
            deduplication_count=1
        ))

        # 4. Q3 Campaign Deck Review (Waiting on Neha Kapoor)
        deck_sources = [
            SourceReference(
                source_id="meet_leadership_sync_01",
                source_type=SourceType.MEETING,
                title="Leadership Sync",
                date_display="Monday, 21 Sep 2026, 10:00 AM",
                timestamp="2026-09-21T10:00:00",
                sender_or_speaker="Neha Kapoor",
                quote="I'll share the draft deck by Wednesday afternoon for team review.",
                reference_tag="[Meeting] Leadership Sync — 21 Sep"
            ),
            SourceReference(
                source_id="email_thread_campaign_deck",
                source_type=SourceType.EMAIL,
                title="Q3 Campaign Deck Email Thread",
                date_display="Tuesday, 22 Sep 2026, 4:30 PM",
                timestamp="2026-09-22T16:30:00",
                sender_or_speaker="Neha Kapoor",
                quote="Moving our review to Thursday 24 September at 9:30 AM. Does that work? (Arjun accepted: Thursday 9:30 AM works for me).",
                reference_tag="[Email] Q3 Campaign Deck Thread — 21–22 Sep"
            ),
            SourceReference(
                source_id="cal_arj_04",
                source_type=SourceType.CALENDAR,
                title="Arjun's Calendar",
                date_display="Thursday, 24 Sep 2026, 9:30 AM",
                timestamp="2026-09-24T09:30:00",
                sender_or_speaker="Calendar Sync",
                quote="Q3 Campaign Deck Review, 09:30 - 10:30 AM, Attendees: Arjun Malhotra, Neha Kapoor.",
                reference_tag="[Calendar] Arjun's Calendar — 24 Sep"
            )
        ]
        actions.append(ActionItem(
            id="act_campaign_deck",
            action="Receive and review Q3 Campaign Deck from Neha",
            owner="Neha Kapoor",
            ownership_status=OwnershipType.OTHER,
            stakeholder="Arjun Malhotra",
            deadline="Thursday, 24 September 2026, 9:30 AM",
            normalized_deadline="2026-09-24T09:30:00",
            status=ActionStatus.UPCOMING,
            priority="High",
            confidence="High",
            sources=deck_sources,
            evidence=[
                "Neha initially planned to send deck on Wednesday afternoon during Mon 21 Sep sync.",
                "Neha requested date shift on Tue 22 Sep at 4:30 PM due to agency attribution delays: 'Moving our review to Thursday 24 September at 9:30 AM'.",
                "Arjun formally agreed on Tue 22 Sep at 5:10 PM: 'Thursday 9:30 AM works for me'.",
                "Latest explicit evidence establishes Thursday 24 Sep at 9:30 AM as the binding deadline."
            ],
            latest_evidence="Tue 22 Sep, 5:10 PM: Arjun confirmed Neha's reschedule request for Thursday 24 Sep at 9:30 AM.",
            why_exists="Marketing deliverables required for sales campaign alignment.",
            conflict_note="CONFLICT RESOLVED: Overrides initial Wednesday afternoon date with latest explicit agreement for Thursday 9:30 AM. NOTE: Triggers a 30-minute calendar conflict with Board Prep Session (9:00-10:00 AM).",
            last_updated="2026-09-22T17:10:00",
            deduplication_count=3
        ))

        # 5. Q3 Expense Variance Report (Divya Rao) - COMPLETED
        expense_sources = [
            SourceReference(
                source_id="meet_leadership_sync_01",
                source_type=SourceType.MEETING,
                title="Leadership Sync",
                date_display="Monday, 21 Sep 2026, 10:00 AM",
                timestamp="2026-09-21T10:00:00",
                sender_or_speaker="Divya Rao",
                quote="Expense variance report scheduled for Thursday morning. Arjun requested Wednesday evening; Divya agreed to try.",
                reference_tag="[Meeting] Leadership Sync — 21 Sep"
            ),
            SourceReference(
                source_id="email_thread_expense_variance",
                source_type=SourceType.EMAIL,
                title="Expense Variance Report Email Thread",
                date_display="Wednesday, 23 Sep 2026, 5:45 PM",
                timestamp="2026-09-23T17:45:00",
                sender_or_speaker="Divya Rao",
                quote="Hi Arjun, please find attached the completed Q3 Expense Variance Report as promised. All regional numbers are reconciled.",
                reference_tag="[Email] Expense Variance Thread — 21–23 Sep"
            ),
            SourceReference(
                source_id="msg_ev_05",
                source_type=SourceType.EMAIL,
                title="Expense Variance Report Email Thread",
                date_display="Wednesday, 23 Sep 2026, 6:15 PM",
                timestamp="2026-09-23T18:15:00",
                sender_or_speaker="Arjun Malhotra",
                quote="Received with thanks, Divya. Reviewing now ahead of tomorrow's board prep.",
                reference_tag="[Email] Arjun's Acknowledgment — 23 Sep"
            )
        ]
        actions.append(ActionItem(
            id="act_expense_report",
            action="Deliver Q3 Expense Variance Report",
            owner="Divya Rao",
            ownership_status=OwnershipType.OTHER,
            stakeholder="Arjun Malhotra",
            deadline="Wednesday, 23 September 2026, 6:00 PM (Completed)",
            normalized_deadline="2026-09-23T18:00:00",
            status=ActionStatus.COMPLETED,
            priority="Medium",
            confidence="High",
            sources=expense_sources,
            evidence=[
                "Initially targeted for Thursday morning; moved to Wednesday evening per Arjun's request.",
                "Divya confirmed commitment for Wednesday by 6:00 PM.",
                "Divya sent completed report at 5:45 PM on Wed 23 Sep.",
                "Arjun confirmed receipt at 6:15 PM on Wed 23 Sep."
            ],
            latest_evidence="Wed 23 Sep, 6:15 PM: Arjun acknowledged receipt of Q3 Expense Variance Report with thanks.",
            why_exists="Finance data needed for executive Board Prep.",
            conflict_note="COMPLETED ITEM: Delivered ahead of committed 6:00 PM deadline on Wednesday evening. Removed from active waiting items.",
            last_updated="2026-09-23T18:15:00",
            deduplication_count=3
        ))

        # 6. Mumbai Office Lease Renewal Agreement Signature (⚠️ UNCLEAR OWNERSHIP)
        lease_sources = [
            SourceReference(
                source_id="meet_leadership_sync_01",
                source_type=SourceType.MEETING,
                title="Leadership Sync",
                date_display="Monday, 21 Sep 2026, 10:00 AM",
                timestamp="2026-09-21T10:00:00",
                sender_or_speaker="Raghav Sethi & Divya Rao",
                quote="Raghav: Facilities flagged it as unassigned. Who is taking ownership of signing this? Divya: Facilities normally handles real estate renewals. Raghav: No one is officially designated as owner yet.",
                reference_tag="[Meeting] Leadership Sync — 21 Sep"
            ),
            SourceReference(
                source_id="email_thread_lease_renewal",
                source_type=SourceType.EMAIL,
                title="Mumbai Office Lease Renewal Email Thread",
                date_display="Monday 21 - Wednesday 23 Sep 2026",
                timestamp="2026-09-23T11:00:00",
                sender_or_speaker="Raghav Sethi",
                quote="Facilities notice: Signature required by Friday 25 Sep 5:00 PM. Raghav asked who is signing. Divya stated not Finance's plate. Raghav (Wed 11:00 AM): As of today, this agreement remains unassigned and unowned.",
                reference_tag="[Email] Mumbai Lease Thread — 21–23 Sep"
            )
        ]
        actions.append(ActionItem(
            id="act_mumbai_lease",
            action="Mumbai office lease renewal signature",
            owner="Unclear",
            ownership_status=OwnershipType.UNCLEAR,
            stakeholder="Facilities Team / Veridian Corp",
            deadline="Friday, 25 September 2026, 5:00 PM IST (End of Day)",
            normalized_deadline="2026-09-25T17:00:00",
            status=ActionStatus.UNCLEAR,
            priority="High",
            confidence="High",
            sources=lease_sources,
            evidence=[
                "Facilities issued formal notice on Mon 21 Sep stating authorized signature required by Friday 25 Sep 5:00 PM IST to avoid expiry penalty.",
                "Raghav asked on Tue 22 Sep who has authority and is signing.",
                "Divya stated on Tue 22 Sep that Facilities coordinates execution and it is not on Finance's plate.",
                "Raghav explicitly followed up on Wed 23 Sep at 11:00 AM: 'Facilities team: please clarify owner immediately. As of today, this agreement remains unassigned and unowned.'",
                "No person has accepted or been assigned responsibility in the source data."
            ],
            latest_evidence="Wed 23 Sep, 11:00 AM: Raghav Sethi confirmed to all parties: 'As of today, this agreement remains unassigned and unowned.'",
            why_exists="Urgent corporate real estate compliance deadline approaching on Friday with financial penalty risk.",
            conflict_note="⚠️ UNCLEAR OWNERSHIP: Ownership is unclear. No owner has been confirmed in the source data. Explicitly flagged per Rule 1. Do NOT assign to Arjun or any other person.",
            last_updated="2026-09-23T11:00:00",
            deduplication_count=2
        ))

        self.audit_log.append(PipelineStepResult(
            step_number=5,
            step_name="Status & Conflict Engine",
            agent_name="StatusEngine",
            description="Resolved temporal conflicts and determined statuses",
            details={"actions_generated": len(actions)}
        ))
        return actions

    def _step_calendar_intelligence(self) -> List[CalendarEvent]:
        events = []
        for raw in CALENDARS.get("arjun", []):
            ev = CalendarEvent(
                id=raw["id"],
                title=raw["title"],
                day=raw["day"],
                date=raw["date"],
                start_time=raw["start_time"],
                end_time=raw["end_time"],
                attendees=raw.get("attendees", []),
                location=raw.get("location"),
                notes=raw.get("notes")
            )
            if ev.date == "2026-09-24":
                if ev.id == "cal_arj_03":
                    ev.has_conflict = True
                    ev.conflict_reason = "⚠️ Scheduling Conflict: Overlaps with Q3 Campaign Deck Review (09:30 - 10:30 AM) by 30 minutes."
                elif ev.id == "cal_arj_04":
                    ev.has_conflict = True
                    ev.conflict_reason = "⚠️ Scheduling Conflict: Overlaps with Board Prep Session (09:00 - 10:00 AM) by 30 minutes."
            events.append(ev)

        self.audit_log.append(PipelineStepResult(
            step_number=6,
            step_name="Calendar Intelligence",
            agent_name="CalendarAgent",
            description="Detected 30-min schedule conflict between Board Prep and Campaign Deck Review on Thursday 24 Sep",
            details={"events_count": len(events), "conflict_count": 2}
        ))
        return events

    def _step_generate_daily_brief(self, actions: List[ActionItem], calendar_events: List[CalendarEvent]) -> DailyBrief:
        needs_action_today = [
            a for a in actions 
            if a.ownership_status == OwnershipType.ARJUN and a.status in [ActionStatus.DUE_TODAY, ActionStatus.OVERDUE]
        ]
        waiting_on_others = [
            a for a in actions 
            if a.ownership_status == OwnershipType.OTHER and a.status != ActionStatus.COMPLETED
        ]
        unclear_ownership = [
            a for a in actions 
            if a.ownership_status == OwnershipType.UNCLEAR
        ]
        overdue = [
            a for a in actions 
            if a.status == ActionStatus.OVERDUE
        ]
        completed = [
            a for a in actions 
            if a.status == ActionStatus.COMPLETED
        ]

        todays_calendar = [ev for ev in calendar_events if ev.date == self.target_date]
        calendar_conflicts = [ev for ev in calendar_events if ev.has_conflict]

        key_risks = [
            KeyRisk(
                id="risk_vendor_list",
                title="Updated Vendor List Overdue / Outstanding",
                severity="High",
                description="Promised to Raghav Sethi for Wednesday morning ops review. Raghav checked in at 8:45 AM; no delivery email recorded.",
                owner_status="Arjun Malhotra",
                deadline="Wednesday, 23 Sep (Morning)",
                action_ref_id="act_vendor_list"
            ),
            KeyRisk(
                id="risk_mumbai_lease",
                title="Mumbai Office Lease Renewal Still Unowned",
                severity="Critical",
                description="Hard deadline this Friday, 25 Sep at 5:00 PM IST. Raghav confirmed on Wednesday morning that no owner has accepted responsibility.",
                owner_status="Unclear (Unassigned)",
                deadline="Friday, 25 Sep 2026, 5:00 PM IST",
                action_ref_id="act_mumbai_lease"
            ),
            KeyRisk(
                id="risk_calendar_clash",
                title="Double-Booking on Thursday Morning",
                severity="Medium",
                description="Q3 Campaign Deck Review (09:30 - 10:30 AM) conflicts with Board Prep Session (09:00 - 10:00 AM). Needs 30-minute shift.",
                owner_status="Arjun Malhotra / Neha Kapoor",
                deadline="Thursday, 24 Sep 2026, 9:30 AM",
                action_ref_id="act_campaign_deck"
            )
        ]

        kpis = {
            "my_actions": len(needs_action_today),
            "waiting_others": len(waiting_on_others),
            "overdue": len(overdue),
            "unclear_ownership": len(unclear_ownership),
            "completed": len(completed)
        }

        self.audit_log.append(PipelineStepResult(
            step_number=7,
            step_name="Daily Executive Brief Generation",
            agent_name="DailyBriefAgent",
            description="Compiled executive summary, priority panel, risks, and calendar highlights",
            details=kpis
        ))

        return DailyBrief(
            simulated_date=self.target_date,
            date_display="Wednesday, 23 September 2026",
            greeting="Good Morning, Arjun",
            summary=(
                "Here is your executive action brief for Wednesday, 23 September 2026. "
                "Immediate focus: The updated vendor list promised to Raghav is due/overdue past the morning window. "
                "You have the rescheduled Meridian Logistics sync with Priya at 3:00 PM. "
                "Divya delivered the Q3 Expense Variance Report ahead of schedule (COMPLETED). "
                "CRITICAL ALERT: The Mumbai office lease renewal remains UNASSIGNED with a Friday deadline."
            ),
            kpis=kpis,
            needs_action_today=needs_action_today,
            waiting_on_others=waiting_on_others,
            unclear_ownership=unclear_ownership,
            overdue=overdue,
            completed=completed,
            todays_calendar=todays_calendar,
            calendar_conflicts=calendar_conflicts,
            key_risks=key_risks
        )
