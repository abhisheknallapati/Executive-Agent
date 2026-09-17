# AI Tools & Reasoning Architecture

## Division of Responsibilities: AI vs Deterministic Engine

| Pipeline Component | Mechanism | Purpose & Implementation | Safety & Verification |
| :--- | :--- | :--- | :--- |
| **Commitment Extraction** | LLM Extraction Agent | Identifies commitments, asks, and promises from natural language text. | Strict Pydantic output schemas; validates speaker identity. |
| **Deadline Normalizer** | LLM + Temporal Rules | Resolves relative time phrases ("Wednesday morning") to exact ISO timestamps. | Bound to 21–25 Sep 2026; never invents times when omitted. |
| **Cross-Source Deduplication** | Hybrid Clustering | Groups commitments across meetings, emails, and voice notes into 1 canonical item. | Preserves all source references behind the consolidated card. |
| **Ownership Classification** | Strict Rule Engine | Separates Arjun's commitments from others; flags unowned items as `UNCLEAR`. | Enforces Rule 1: Never guess or invent an owner. |
| **Status Resolution Engine** | Deterministic Engine | Compares current simulated timestamp against deadlines and delivery proofs. | Enforces Rule 3: Explicit receipt proof required for `COMPLETED`. |
| **Calendar Intelligence** | Interval Overlap Engine | Compares meeting time intervals on Arjun's calendar. | Flags clashes (e.g. Board Prep vs Deck Review) without silent edits. |
| **Grounded Q&A Agent** | Grounded RAG | Retrieves structured action records and formats answers with citations. | Enforces Rule 6 & 7: Cites verbatim quotes; refuses if data is absent. |

## Seven Hallucination Safeguards
1. **Rule 1**: Never invent an owner.
2. **Rule 2**: Never invent a deadline.
3. **Rule 3**: Never mark an action completed without explicit receipt evidence.
4. **Rule 4**: Prefer the latest explicit statement when resolving conflicts.
5. **Rule 5**: If conflicting information cannot be resolved, surface the conflict.
6. **Rule 6**: Every important answer must contain source evidence.
7. **Rule 7**: If source data doesn't answer a question, respond with standard refusal.
