# AI Governance & Model Risk Assessment Report
**Organization:** Falak Pay Financial Company (fictional entity, lab use)
**Assessment Date:** *[generated from seeded demo data]*
**Scope note:** This assessment extends GRC first principles to AI/ML systems; it does not cite specific SAMA CSF or NCA ECC control numbers, as neither framework yet defines a dedicated AI control domain.
**Classification:** Confidential — Internal Use Only

---

## 1. Executive Summary
Falak Pay tracks **5 AI systems** with a weighted sample accuracy of **90.4%** across all logged review batches. This aggregate, sampled figure — not a single pass/fail test — is the evidence base for systems whose output is not deterministic.

The most significant finding is a **direct replay of the 2022–2024 Air Canada chatbot pattern**: the Customer Support Chatbot's "Refund / Policy Exception Escalation" checkpoint was documented in the design specification but **not enforced in production**, resulting in an incident where the chatbot gave a customer inaccurate information about a fee waiver policy. The chatbot's own sample accuracy dropped to **76%** in the review batch immediately preceding this incident — a leading indicator that, in hindsight, should have triggered faster remediation.

## 2. Scope & Methodology
- **Scope:** 5 AI systems, 5 oversight checkpoints, 7 sample review batches, 2 incidents, 5 model changes
- **Reference case:** Air Canada chatbot ruling, 2024 — used as the structural benchmark for AI oversight-checkpoint enforcement gaps
- **Tooling:** AI Governance & Model Risk Evidence Tracker (this lab's application)
- **Methodology note:** Because AI outputs vary run-to-run, this assessment relies on periodic statistical sampling rather than exhaustive testing — the sample accuracy rate is treated as the primary evidence metric, analogous to how a financial audit relies on sampled transaction testing rather than reviewing every transaction.

## 3. Key Metrics
| Metric | Value |
|---|---|
| AI systems tracked | 5 |
| Weighted sample accuracy (all systems) | 90.4% |
| Escalation-needed rate (all samples) | ~3.9% |
| Open incidents | 1 |
| Unenforced oversight checkpoints | 2 |
| Model changes pending approval | 2 |

## 4. Critical Finding — Air Canada Pattern Replay

### Finding: Chatbot Escalation Checkpoint Documented But Not Enforced
- **System:** Customer Support Chatbot (Critical risk tier)
- **Checkpoint:** Refund / Policy Exception Escalation — designed to hand off to a human whenever refunds, compensation, or policy exceptions come up
- **What happened:** The checkpoint existed in the design specification but was never actually implemented as a hard technical control in the production build. A customer asked about a fee waiver; the chatbot gave inaccurate information about the waiver process; the customer relied on it and disputed a subsequent charge.
- **Leading indicator that was available but not acted on fast enough:** The February sample review batch (n=50) showed accuracy had dropped to 76%, with 9 outputs flagged as needing escalation that didn't receive it — a clear statistical warning sign a month before the incident was reported.
- **Direct parallel to Air Canada:** Structurally identical — a customer-facing AI system gave policy-inconsistent information on a sensitive topic, with no enforced human checkpoint to catch it, and the organization only responded after a customer-facing dispute rather than its own monitoring.
- **Recommendation:** This assessment recommends treating **sample accuracy drops as a leading indicator requiring the same urgency as a Critical vulnerability finding** (see Lab 03's SLA model) — not something reviewed only during a scheduled cadence.

## 5. Other Notable Findings
| System | Finding | Status |
|---|---|---|
| Internal Developer Copilot | Security-Sensitive Code Suggestion Review checkpoint not yet enforced | Open — planned for next quarter |
| Fraud Anomaly Detection Model | Accuracy improved from 94% to 96% after Q1 retraining on seasonal data | Resolved, demonstrating the model-change/retrain cycle working correctly |

## 6. Well-Managed Examples (for contrast)
- **Credit Scoring Model:** All automated declines require human loan-officer review before communication — no automated denial is ever sent directly from the model. Checkpoint fully enforced.
- **Fraud Anomaly Detection Model:** High-value transaction blocks remain advisory only, with the Checker role (see Lab 02) retaining final authority — model output never unilaterally executes a block above the defined threshold.

## 7. Root Cause Themes
1. **A gap between documented design intent and enforced production behavior** — the single highest-risk pattern, and the direct cause of the Air Canada-pattern incident.
2. **Sample accuracy trends were available but not treated with escalation urgency** — the leading indicator existed a month before the customer-facing incident.
3. **Checkpoints on newer or lower-profile systems (Developer Copilot) lag behind those on customer-facing Critical systems** — a resourcing/prioritization gap, not a conceptual one.

## 8. Recommendations & Roadmap
| Priority | Action | Owner | Target Date |
|---|---|---|---|
| P1 | Enforce the Refund / Policy Exception checkpoint as a hard technical block (Model Change already logged, Pending) | Omar Al-Shammari | Within 1 week |
| P1 | Define a sample-accuracy SLA: any batch below 85% triggers mandatory review within 5 business days, analogous to Lab 03's patch SLA | Khalid Al-Mutairi | Next policy review |
| P2 | Enforce Security-Sensitive Code Suggestion Review checkpoint on the Developer Copilot | Layla Al-Ghamdi | Next quarter |
| P3 | Extend sample review cadence to the Marketing Content Generator, currently untested | Reem Al-Subai'i | Next quarter |

## 9. Conclusion
Falak Pay's AI governance program correctly implements the core principle this lab is built around: evidence for a non-deterministic system comes from sampled, trended, aggregate data, not a single static check. That evidence base is what surfaced the Air Canada-pattern gap in the first place — the February sample batch showed the accuracy drop before the customer complaint did. The remaining work is tightening the response loop so a statistical warning sign triggers action as urgently as a security incident would.

## 10. Sign-off
| Name | Role | Date |
|---|---|---|
| Khalid Al-Mutairi | CISO | |
| Board Risk & Compliance Committee Chair | | |

---
*This report was generated against the seeded demo dataset in this lab (`seed_demo_data.py`). Regenerate the live version anytime via the app's `/report` view.*
