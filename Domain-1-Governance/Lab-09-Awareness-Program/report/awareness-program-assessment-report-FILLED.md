# Security Awareness Program Assessment Report
**Organization:** Falak Pay Financial Company (fictional entity, lab use)
**Assessment Date:** *[generated from seeded demo data]*
**Maps to:** SAMA CSF 1.6, 1.7 | NCA ECC 1‑10 | **Classification:** Confidential — Internal Use Only

---

## 1. Executive Summary
Falak Pay's Security Awareness Program tracks **12 employees** across 8 role-based courses, with an overall training completion rate of approximately **78%**. Two employees are flagged as **repeat simulation offenders**, and — most critically — one **privileged employee provided credentials during a simulated vishing call**, a direct structural replay of the 2020 Twitter breach pattern.

This finding should be treated as the top priority in this assessment cycle: it demonstrates that Falak Pay's current employee base includes at least one instance of exactly the vulnerability that enabled one of the most consequential social-engineering breaches in recent history.

## 2. Scope & Methodology
- **Scope:** 12 employees across 6 departments, 8 training courses, 3 simulation campaigns (2 email phishing, 1 vishing)
- **Reference case:** Twitter, July 2020 — used as the structural benchmark for vishing/social-engineering risk
- **Tooling:** Security Awareness & Training Program Tracker (this lab's application)

## 3. Key Metrics
| Metric | Value |
|---|---|
| Employees tracked | 12 |
| Overall training completion | ~78% |
| Overdue training assignments | 2 |
| Repeat simulation offenders | 2 |
| Privileged employees who failed a vishing simulation | 1 |
| Vishing campaign failure rate | ~33% (2 of 6 tested employees) |

## 4. Critical Finding — Twitter Pattern Replay

### Finding: Privileged Employee Provided Credentials During Simulated Vishing Call
- **Employee:** Sara Al-Dosari, IT Support Specialist (privileged access)
- **Campaign:** Q1 2026 Vishing — Fake IT Support Credential Reset
- **What happened:** During a simulated phone call impersonating IT support and requesting a "password confirmation" to resolve a fake account lockout, this employee provided credentials.
- **Direct parallel to Twitter:** This is structurally identical to the 2020 breach — a privileged employee, socially engineered over the phone by a caller impersonating IT support, providing the access an attacker asked for.
- **Compounding factor:** This same employee's Vishing & Social Engineering Awareness training assignment is currently **Overdue**, meaning the relevant training had not been completed before the simulation exposed the gap.
- **Recommendation:** Immediate mandatory retraining, followed by a re-test simulation within 30 days. Review whether this employee's help-desk role requires a stricter identity-verification procedure for credential/access reset requests, independent of individual training completion.

## 5. Other Notable Findings

### Repeat Offender: Huda Al-Anazi (Support Team Lead, privileged)
Failed two separate simulations — one email phishing (Q2) and one vishing (Q1), where she engaged with the caller and described her role/access before disengaging without providing credentials or reporting the call. Given her privileged access and team-lead role, this pattern warrants targeted follow-up.

### Positive Example: Noura Al-Qahtani (Head of Payments Operations, privileged)
Correctly identified and reported both the Q1 email phishing simulation and the vishing simulation — a model response demonstrating the awareness program's content is effective when actually internalized.

### New Hire Handling
Bilal Al-Rashid (new hire, Q1 2026) failed the Q1 email phishing simulation by providing credentials, but after completing follow-up training, correctly reported the Q2 simulation — a clear before/after example of training effectiveness.

## 6. Root Cause Themes
1. **Vishing resistance is measurably weaker than email phishing resistance** — the vishing campaign's failure rate among tested employees was notably higher than the email campaigns', consistent with the industry-wide gap this lab is built around.
2. **Training completion gaps correlate with simulation failures** — both flagged privileged-risk employees had incomplete or overdue Vishing & Social Engineering Awareness training at the time of their respective simulations.
3. **Positive trend on repeat testing** — employees who failed an initial simulation and then completed follow-up training (e.g., Bilal Al-Rashid) showed improved performance on subsequent tests, validating the assign-test-retrain cycle.

## 7. Recommendations & Roadmap
| Priority | Action | Owner | Target Date |
|---|---|---|---|
| P1 | Mandatory retraining + re-test for Sara Al-Dosari (privileged vishing failure) | Khalid Al-Mutairi | Within 2 weeks |
| P1 | Review/strengthen identity-verification procedure for IT support credential/access requests | Fatimah Al-Zahrani | Within 1 month |
| P2 | Targeted follow-up for repeat offender Huda Al-Anazi | Khalid Al-Mutairi | Within 1 month |
| P2 | Close the 2 overdue training assignments | Awareness Program Owner | Within 2 weeks |
| P3 | Increase vishing simulation frequency to quarterly (currently less frequent than email phishing) | Khalid Al-Mutairi | Next program review |

## 8. Conclusion
Falak Pay's awareness program demonstrates real, measured effectiveness in several cases — correct reporting behavior from senior staff, and improvement after follow-up training for a new hire. The vishing simulation, however, surfaced exactly the risk pattern behind the 2020 Twitter breach: a privileged employee, under social pressure over the phone, provided access an attacker asked for. Closing this specific gap, and extending vishing testing to match the rigor already applied to email phishing, is the clear priority for the next program cycle.

## 9. Sign-off
| Name | Role | Date |
|---|---|---|
| Khalid Al-Mutairi | CISO | |
| Board Risk & Compliance Committee Chair | | |

---
*This report was generated against the seeded demo dataset in this lab (`seed_demo_data.py`). Regenerate the live version anytime via the app's `/report` view.*
