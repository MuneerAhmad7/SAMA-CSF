# Security Team Training &amp; Certification Assessment Report
**Organization:** Falak Pay Financial Company (fictional entity, lab use)
**Assessment Date:** *[generated from seeded demo data]*
**Deepens:** SAMA CSF 1.7 | **Classification:** Confidential — Internal Use Only

---

## 1. Executive Summary
Falak Pay's security team of **6 members** has 15 tracked skill assessments across 6 technical specialties, with **10 open gaps** (current level below required level). The widest gap — a Critical, 2-level deficiency in **Digital Forensics on the SOC Analyst role** — is a direct structural replay of the governance failure behind the 2015 OPM breach: a known technical capability gap, cross-referenced with a Critical finding already flagged in Lab 11's audit register, that had no funded training plan item addressing it until this cycle.

Of 8 tracked certifications, **1 is Expired** (a required credential) and **1 is Expiring Soon** — both held by the same team member, the organization's most senior Incident Responder. Training plan completion stands at 12.5% (1 of 8 items), with 1 item currently Delayed due to budget approval timing.

## 2. Scope &amp; Methodology
- **Scope:** 6 security team members, 6 technical specialties, 8 certifications, 8 training plan items
- **Reference case:** OPM, breach discovered 2015 — used as the structural benchmark for unaddressed technical capability gaps
- **Tooling:** Security Team Training &amp; Certification Plan Tracker (this lab's application)
- **Distinction from Lab 09:** This assessment covers the technical security function specifically, not general staff awareness — SAMA CSF 1.7's certification and technical-training requirements are a distinct, deeper obligation from 1.6's awareness requirements.

## 3. Key Metrics
| Metric | Value |
|---|---|
| Security team members | 6 |
| Skill assessments recorded | 15 |
| Open skill gaps | 10 |
| Widest single gap | 2 levels (Digital Forensics, Sara Al-Dosari) |
| Expired certifications | 1 |
| Certifications expiring within 90 days | 1 |
| Training plan completion | 12.5% (1/8) |
| Total training budget allocated | SAR 23,700 |

## 4. Critical Finding — OPM Pattern Replay

### Finding: Digital Forensics Capability Gap on the SOC Team
- **Team member:** Sara Al-Dosari, SOC Analyst
- **Gap:** Current level Novice (1), required level Proficient (3) — a 2-level deficiency, the widest in the organization
- **Cross-reference:** This gap was already flagged as a technical capability weakness in Lab 11's FY2025 Internal Cybersecurity Audit findings register.
- **Direct parallel to OPM:** Structurally identical to the pattern the U.S. congressional oversight report identified — a documented, known technical capability gap on the security team that persisted without a funded remediation plan.
- **Status at time of this assessment:** A training plan item (GCFA Digital Forensics Certification Prep, SAR 8,500) has now been logged and is Planned — this assessment recommends treating its completion as a tracked priority, not a routine training line item.

## 5. Certification Findings
| Team Member | Certification | Status | Note |
|---|---|---|---|
| Fatimah Al-Zahrani | CISSP | **Expired** | Required for role; renewal should be prioritized alongside her GCFA recertification (already In Progress) |
| Fatimah Al-Zahrani | GCFA | Expiring Soon (&lt;90 days) | Recertification already logged as an In Progress training plan item |

Both lapses belong to the same individual — the organization's most senior Incident Responder and de facto Digital Forensics mentor. This concentration of risk in one person is itself worth noting: her expertise appears difficult to backfill quickly, which raises the stakes on both her own recertification and on closing Sara Al-Dosari's parallel gap in the same specialty.

## 6. Well-Managed Examples (for contrast)
- **Khalid Al-Mutairi (CISO):** All skill levels meet or exceed role requirements; both CISSP and CISM certifications Active with substantial validity remaining.
- **Yousef Bin-Nasser (Penetration Tester):** OSCP held and Active; a further OSCP-related training plan item (exam retake preparation) is already In Progress, demonstrating continuous investment beyond the baseline credential.

## 7. Root Cause Themes
1. **A known gap (Digital Forensics) existed in both the audit findings register (Lab 11) and the skills matrix without a funded plan connecting the two** until this assessment cycle — the specific failure mode this lab is built to close.
2. **Certification expiry risk is concentrated in a single, hard-to-replace specialist**, which is a business-continuity risk as much as a compliance one.
3. **Budget approval timing, not lack of intent, caused the one Delayed training item** — a process gap rather than a resourcing gap.

## 8. Recommendations &amp; Roadmap
| Priority | Action | Owner | Target Date |
|---|---|---|---|
| P1 | Complete Fatimah Al-Zahrani's CISSP renewal (already expired) | Fatimah Al-Zahrani / Khalid Al-Mutairi | Within 30 days |
| P1 | Fund and track the GCFA Digital Forensics Certification Prep for Sara Al-Dosari to closure, not just to Planned status | Khalid Al-Mutairi | Per logged target date |
| P2 | Resolve the budget approval delay on the SANS Cloud Security Conference item | Khalid Al-Mutairi | Within 2 weeks |
| P2 | Cross-train a second team member in Digital Forensics to reduce single-person concentration risk | Khalid Al-Mutairi | Next planning cycle |
| P3 | Establish a standing quarterly review linking Lab 11 audit findings directly to new Skills Matrix entries | Khalid Al-Mutairi | Next Committee meeting |

## 9. Conclusion
Falak Pay's technical security team shows real strength in several specialties, and the training plan process is functioning — items are being logged, budgeted, and in most cases progressed. The one finding that matters most is also the most instructive: a capability gap identified through one assurance mechanism (Lab 11's audit) had not yet been connected to a funded plan through this one, until now. That connection — audit finding to skills matrix to funded training item — is the entire point of this lab, and closing it before it becomes a multi-year gap is the direct lesson of the OPM case.

## 10. Sign-off
| Name | Role | Date |
|---|---|---|
| Khalid Al-Mutairi | CISO | |
| Board Risk &amp; Compliance Committee Chair | | |

---
*This report was generated against the seeded demo dataset in this lab (`seed_demo_data.py`). Regenerate the live version anytime via the app's `/report` view.*
