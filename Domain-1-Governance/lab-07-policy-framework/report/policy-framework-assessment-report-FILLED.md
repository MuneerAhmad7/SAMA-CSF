# Policy Framework Assessment Report
**Organization:** Falak Pay Financial Company (fictional entity, lab use)
**Assessment Date:** *[generated from seeded demo data]*
**Maps to:** SAMA CSF 1.3 / 4.2, NCA ECC 1‑3 / 4‑1 | **Classification:** Confidential — Internal Use Only

---

## 1. Executive Summary
Falak Pay's Policy Register contains **14 documents** (1 Master Policy, 10 Domain Policies, 2 Standards, 2 Procedures — note some documents serve dual roles). Control Domain Coverage stands at **72.7% (8/11 domains)**, with three domains currently lacking an Approved/Published policy: **Third-Party & M&A Security** (in Draft), **Physical Security** (stuck in Review), and **Cloud Security** (no policy exists at all).

The Data Classification & Protection Policy is **currently overdue for its scheduled review** — flagged automatically on the Dashboard. Of three tracked entities in the M&A/Third-Entity Integration Register, one — a recent acquisition — sits at only **42% policy integration**, directly mirroring the Marriott/Starwood pattern this lab is built around.

## 2. Scope & Methodology
- **Scope:** Full Falak Pay policy hierarchy, 11 required control domains, 3 tracked entities (subsidiary, acquisition, third-party partner)
- **Reference case:** Marriott/Starwood, disclosed 2018 — used as the structural benchmark for M&A policy integration
- **Tooling:** Policy Framework Manager (this lab's application)

## 3. Key Metrics
| Metric | Value |
|---|---|
| Total policies/standards/procedures | 14 |
| Currently Published | 9 |
| Control domain coverage | 72.7% (8/11) |
| Overdue policy reviews | 1 |
| Tracked entities | 3 |
| Average entity integration | 71.7% |
| Entities below 70% integration (at risk) | 1 |

## 4. Coverage Gaps

### Gap 1: No Cloud Security Policy
- **Risk:** Falak Pay has active cloud infrastructure (referenced across Labs 01–05) with no governing policy at all — not draft, not overdue, simply absent.
- **Recommendation:** Draft a Cloud Security Policy immediately; this is the single most exposed domain in the framework.

### Gap 2: Third-Party & M&A Security Integration Policy Still in Draft
- **Risk:** This is the exact policy category that was reportedly missing or delayed in the Marriott/Starwood integration. Falak Pay is drafting it proactively, which is the right instinct — but until it's Approved and Published, the organization has no formal, enforceable standard for integrating acquired entities' security postures.
- **Recommendation:** Prioritize this policy's approval given the active, under-integrated acquisition already in the Entity Register (see Finding below).

### Gap 3: Physical Security Standard Stuck in Review
- **Risk:** Under review following an office relocation — low urgency but should not be allowed to stall indefinitely.
- **Recommendation:** Set a hard target date for exiting Review status.

## 5. Overdue Review Finding
**Data Classification & Protection Policy (v1.4)** is past its scheduled review date. Given this policy governs how sensitive data (including payment and customer data) is classified and handled, this should be treated as a near-term priority, not a routine backlog item.

## 6. M&A / Entity Integration Finding — Najm Instant Transfer (Recent Acquisition)
- **Integration level:** 42% — the lowest of any tracked entity, and below the 70% risk threshold.
- **Specific gaps noted:** Data Classification, Cryptography, and Incident Response policies not yet extended to Najm's legacy systems; no unified monitoring across the combined estate.
- **Direct parallel to Marriott/Starwood:** This is precisely the scenario — an acquired entity's systems continuing to operate under pre-acquisition standards, with no enforced timeline for harmonization.
- **Recommendation:** Fast-track approval of the Third-Party & M&A Security Integration Policy (Gap 2 above) specifically to give this integration a hard, tracked deadline rather than an open-ended "eventually."

## 7. Recommendations & Roadmap
| Priority | Action | Owner | Target Date |
|---|---|---|---|
| P1 | Draft and approve Cloud Security Policy | Khalid Al-Mutairi | Next quarter |
| P1 | Approve Third-Party & M&A Security Integration Policy; apply it retroactively to Najm integration with a hard deadline | Khalid Al-Mutairi | Next Board Risk Committee meeting |
| P1 | Complete overdue review of Data Classification & Protection Policy | Fatimah Al-Zahrani | Within 30 days |
| P2 | Move Physical Security Standard out of Review status | Omar Al-Shammari | Next quarter |
| P2 | Raise Najm Instant Transfer integration above 70% | Khalid Al-Mutairi + Najm integration team | Two quarters |

## 8. Conclusion
Falak Pay's policy framework has strong foundational coverage (72.7%, with core domains like Governance, IAM, Cryptography, and Incident Response fully published), but three specific, identifiable gaps — Cloud Security, Third-Party & M&A Security, and one under-integrated acquisition — represent exactly the pattern that led to the Marriott/Starwood breach if left unaddressed. Unlike Starwood, Falak Pay already has visibility into this gap via this register; the remaining work is executing against it on a defined timeline.

## 9. Sign-off
| Name | Role | Date |
|---|---|---|
| Khalid Al-Mutairi | CISO | |
| Board Risk & Compliance Committee Chair | | |

---
*This report was generated against the seeded demo dataset in this lab (`seed_demo_data.py`). Regenerate the live version anytime via the app's `/report` view.*
