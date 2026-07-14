# LinkedIn Post Draft — Lab 10

---

**Main version**

A comment on one of my earlier posts in this series stuck with me: "SAMA CSF and NCA ECC assume you can point to a deterministic control, but how do you evidence Board oversight of a workflow whose output changes every run? Nobody's built a tracker for that yet."

So I built one.

Every control in this series so far has been deterministic: a policy is Published or it isn't (Lab 01), a patch is within SLA or it isn't (Lab 03), a Deploy gate Passed or was Waived (Lab 08). An auditor can point at one record and get a yes/no answer.

AI systems don't work that way. The same prompt can produce a different answer every time. In 2024, a Canadian tribunal ruled against Air Canada after its website chatbot gave a customer incorrect information about a bereavement fare — Air Canada's own defense argued the chatbot was "a separate legal entity" responsible for its own words. The tribunal didn't buy it. But the case exposed something real: **most organizations don't yet have a way to evidence oversight of a system that behaves probabilistically.**

**Lab 10: AI Governance & Model Risk Evidence Tracker** — and the core design idea is different from every other lab in this series:

→ Instead of a binary control check, the headline metric is a **weighted sample accuracy rate** — you can't test every possible output, so you sample real outputs periodically, score them against a rubric, and trend the rate over time. That trended number *is* the Board evidence.
→ **Human Oversight Checkpoints** per AI system — documented triggers where the system must hand off to a human — with an explicit enforced/not-enforced flag, because a checkpoint that only exists in a design doc doesn't count.
→ An **Incident Log** treating AI failures exactly like security incidents — root cause, remediation, ownership.
→ A **Model Change Log** — the AI-specific equivalent of a Deploy gate, gating prompt/model/guardrail changes through approval.

I seeded it with a direct replay of the Air Canada pattern: a customer support chatbot with a "refund/policy exception" escalation checkpoint that existed in the design spec but was never actually enforced in production. The sample accuracy batch a month before the resulting incident had already dropped to 76% — the warning sign was there in the data, it just wasn't treated with the urgency a security finding would get.

This lab comes with an explicit disclaimer the rest of the series doesn't need: it doesn't cite a SAMA CSF or NCA ECC control number, because neither framework has caught up to this yet. That's not a weakness in the lab — that's the actual point being made.

Full code, case study, policy template, and a completed assessment report are on GitHub — link in comments.

#CyberSecurity #GRC #AIGovernance #ModelRisk #SAMA #NCA #InfoSec #SaudiArabia #ResponsibleAI #RiskManagement

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Dashboard's accuracy gauge next to the "unenforced checkpoint" alert banner.
- A second image of the Sample Review Log showing the accuracy trend (92% → 76% → 82%) across the three chatbot batches tells the leading-indicator story visually.
- Consider tagging or quoting (with permission) whoever left the original comment that inspired this lab — good-faith engagement like that deserves credit.
- GitHub link goes in the first comment, not the post body.
