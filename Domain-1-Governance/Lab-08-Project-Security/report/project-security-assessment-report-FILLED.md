# Project Security Assessment Report
**Organization:** Falak Pay Financial Company (fictional entity, lab use)
**Assessment Date:** *[generated from seeded demo data]*
**Maps to:** SAMA CSF 1.5, 3.2 | NCA ECC 1‑6, 2‑8 | **Classification:** Confidential — Internal Use Only

---

## 1. Executive Summary
Falak Pay currently tracks **6 projects** through the Security Gate Pipeline, with **overall gate compliance at approximately 72%** across all phases. One project — **Payment Checkout Redesign** — has a **Waived Deploy gate**, followed by an **ungated production change** to the live payment page. This is a direct structural replay of the 2018 British Airways breach pattern and represents the single highest-priority finding in this assessment.

The Third-Party Script Register additionally identifies **4 scripts without SRI integrity protection**, including one running on the same payment page (`analytics-tracker.js`), unreviewed for over 7 months at time of assessment.

## 2. Scope & Methodology
- **Scope:** 6 tracked projects, 36 security gates, 8 third-party scripts, 4 logged production changes
- **Reference case:** British Airways, disclosed 2018 — used as the structural benchmark for SDLC/change-management risk
- **Tooling:** Project Security Gate Tracker (this lab's application)

## 3. Key Metrics
| Metric | Value |
|---|---|
| Projects tracked | 6 |
| Total security gates | 36 |
| Gates Passed | ~26 |
| Overall gate compliance | ~72% |
| Changes deployed without a passed Deploy gate | 1 |
| Third-party scripts without SRI protection | 4 (1 on a Critical-risk page) |

## 4. Critical Finding — British Airways Pattern Replay

### Finding: Payment Checkout Redesign — Deploy Gate Waived, Followed by Ungated Change
- **Project:** Payment Checkout Redesign (Critical criticality, Payments business unit)
- **What happened:** Under release deadline pressure, the Deploy gate for this project was marked **Waived** rather than Passed. Subsequently, a hotfix to the analytics tracking script was **deployed directly to the live payment page** without going back through a formal Deploy gate review.
- **Direct parallel to British Airways:** This is structurally identical to the 2018 breach — a change reaching the live payment page without a rigorous security sign-off, on a page where a malicious or careless script could silently capture card data.
- **Compounding factor:** The `analytics-tracker.js` script running on this same page has no SRI hash pinned and has not been reviewed in over 7 months, meaning there is currently **no integrity control** that would detect if this script's behavior changed unexpectedly.
- **Recommendation:** Treat as an emergency finding. Require immediate retroactive security review of the deployed hotfix, close the SRI gap on all payment-page scripts, and revise change management process so "Waived" gates cannot be followed by unreviewed production changes without a documented emergency-change exception (see Change Management Policy, Section on emergency exceptions).

## 5. Other Notable Gate Findings
| Project | Gate | Status | Note |
|---|---|---|---|
| Customer Support Chatbot | Build | Failed | Chatbot found logging unredacted card numbers accidentally pasted into chat — sent back for remediation. Process working as intended. |
| Third-Party Loyalty Program Integration | Build | In Progress | Vendor API integration code under active review. |

## 6. Well-Managed Examples (for contrast)
- **Core Banking DB Migration:** All 6 gates Passed, including a completed Post-Implementation review — the process working exactly as designed for a Critical-criticality project.
- **Mobile Banking App v3.0:** Full Deploy gate sign-off obtained before App Store submission, with a 30-day post-launch review scheduled.

## 7. Root Cause Themes
1. **Deadline pressure leading to gate waivers on Critical, customer-facing projects** — the single highest-risk pattern identified, and the direct cause of the BA-pattern replay.
2. **Third-party scripts onboarded once and never re-reviewed** — 4 of 8 tracked scripts have no SRI protection, several unreviewed for 6+ months.
3. **No hard technical control preventing an ungated change from reaching a Waived-gate project** — the process depends on individual discipline rather than an enforced control.

## 8. Recommendations & Roadmap
| Priority | Action | Owner | Target Date |
|---|---|---|---|
| P1 | Retroactive security review of the payment-page hotfix; close analytics-tracker.js SRI gap | Yousef Al-Harbi + Fatimah Al-Zahrani | Within 48 hours |
| P1 | Formal Deploy gate re-review for Payment Checkout Redesign — Waived status is not acceptable for a Critical payment project | Khalid Al-Mutairi | Within 1 week |
| P2 | SRI-pin all remaining unprotected scripts, prioritizing Critical/High-risk pages | Project owners | Within 2 weeks |
| P2 | Define and communicate a formal emergency-change exception process distinct from a "Waived" gate | Khalid Al-Mutairi | Next policy review |
| P3 | Quarterly re-review cadence for all third-party scripts on customer-facing pages | Layla Al-Ghamdi | Ongoing |

## 9. Conclusion
Falak Pay's project security gate process functions correctly in the majority of cases — the Customer Support Chatbot finding shows the Build gate catching a real issue, and Core Banking DB Migration shows full lifecycle discipline on a Critical project. The Payment Checkout Redesign finding is the exception that matters most: it demonstrates exactly how deadline pressure can recreate the precise structural failure behind the British Airways breach, even inside an organization with a documented gate process — because a documented process only works if it can't be quietly bypassed under pressure.

## 10. Sign-off
| Name | Role | Date |
|---|---|---|
| Khalid Al-Mutairi | CISO | |
| Board Risk & Compliance Committee Chair | | |

---
*This report was generated against the seeded demo dataset in this lab (`seed_demo_data.py`). Regenerate the live version anytime via the app's `/report` view.*
