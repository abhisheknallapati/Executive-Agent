# Sources & Assumptions: Executive Productivity Agent (AIONOS)

## Ground Truth Data Sources
The system operates exclusively on the verified assignment dataset covering **Monday, 21 September 2026 – Friday, 25 September 2026**:
1. **Meeting Transcript**:
   - `Leadership Sync` (21 Sep 2026, 10:00–11:00 AM)
   - Attendees: Arjun Malhotra, Neha Kapoor, Raghav Sethi, Divya Rao.
2. **Email Threads**:
   - `Vendor List`: Raghav & Arjun (21–23 Sep)
   - `Q3 Campaign Deck`: Neha & Arjun (21–22 Sep)
   - `Meridian Logistics Reschedule`: Priya Nair & Arjun (21–22 Sep)
   - `Expense Variance Report`: Divya & Arjun (21–23 Sep)
   - `Mumbai Office Lease Renewal`: Facilities, Raghav, Divya, Arjun (21–23 Sep)
3. **Voice Notes**:
   - `Voice Note 1` (Recorded Mon 21 Sep 6:30 PM by Arjun)
   - `Voice Note 2` (Recorded Tue 22 Sep 8:45 AM by Arjun)
4. **Stakeholder Calendars**:
   - Arjun Malhotra, Neha Kapoor, Raghav Sethi, Divya Rao.

## Core System Assumptions
1. **Target Executive**: The user is Arjun Malhotra, VP Sales at Veridian Corp (`arjun.malhotra@veridian-corp.example`).
2. **Simulated Daily Brief Date**: Wednesday, 23 September 2026.
3. **Temporal Ordering & Precedence (Rule 4)**: Where plans evolve, the latest explicit communication overrides older statements.
   - Example: Neha moving the deck review to Thursday morning overrides the earlier Wednesday afternoon target.
4. **Completion Proof (Rule 3)**: A commitment cannot be marked `COMPLETED` without explicit evidence of delivery or receipt.
   - Divya sent the variance report on Wednesday at 5:45 PM -> `COMPLETED`.
   - Arjun did not send the vendor list -> `OVERDUE` / `AT RISK`.
5. **Ownership Rigor (Rule 1)**: The system NEVER guesses or assigns ownership based on inference.
   - For the Mumbai Lease Renewal, because no stakeholder has accepted ownership, it is strictly flagged as `⚠️ UNCLEAR OWNERSHIP`.
6. **Information Boundary (Rule 7)**: The agent strictly refuses to invent answers when source data is silent.
