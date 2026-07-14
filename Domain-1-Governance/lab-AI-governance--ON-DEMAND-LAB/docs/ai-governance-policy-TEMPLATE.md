# AI Governance & Model Risk Policy
**Scope note:** This policy extends existing governance, risk, and change-management principles to AI/ML systems. It does not map to a specific SAMA CSF or NCA ECC control number, as neither framework yet defines a dedicated AI control domain — this is deliberate, forward-looking practice.

## 1. Purpose
Ensure every AI/ML system in use has a named owner, a risk classification, enforced human oversight where required, and evidence of ongoing quality — recognizing that AI outputs are non-deterministic and cannot be evidenced with a single pass/fail test.

## 2. AI System Inventory Requirement
Every AI/ML system — whether customer-facing, internal, or embedded in another product — must be registered with:
- A named accountable owner
- A risk tier (Critical/High/Medium/Low) based on customer-facing impact and decision autonomy
- Current model/prompt version

## 3. Human Oversight Checkpoints
Every Critical or High risk-tier AI system must have documented, **and technically enforced**, checkpoints where the system hands off to a human for defined trigger conditions (e.g., refunds, account closures, automated declines, high-value transactions). A checkpoint that exists only in a design document, and not in the running system, does not satisfy this requirement — this is the exact gap behind the Air Canada chatbot ruling.

## 4. Output Sample Review (the core evidence mechanic)
Because AI output varies per run, exhaustive testing is not possible. Instead:
- Each AI system undergoes periodic (minimum monthly for Critical, quarterly for High/Medium) sampling of real outputs.
- A defined reviewer scores each sampled output as Accurate, Inaccurate, or Escalation Needed against a written rubric.
- The resulting accuracy rate is tracked over time. **Any sample batch scoring below 85% accuracy is treated with the same urgency as a Critical vulnerability finding** and triggers mandatory review within 5 business days.

## 5. Incident Handling
Any AI output that causes a real customer, financial, or operational problem is logged and tracked exactly like a security incident — with root cause analysis and remediation — regardless of whether the underlying system is "just a chatbot" or a core financial model.

## 6. Model Change Control
Any change to a model version, prompt, or guardrail configuration for a Critical or High risk-tier system requires documented approval before reaching production — the AI-specific equivalent of a Deploy gate (see Lab 08).

## 7. Review
Reviewed annually or immediately following any AI-related incident.

---
*This is a plain-document policy template. The lab's app (`src/`) tracks live sample reviews, checkpoints, and incidents, and can generate a printable audit report at `/report`.*
