# Regulatory Compliance Assessment Report
**Organization:** Falak Pay Financial Company (fictional entity, lab use)
**Assessment Date:** *[generated from seeded demo data]*
**Maps to:** SAMA CSF 1.9, NCA ECC 1‑7, PDPL | **Classification:** Confidential — Internal Use Only

---

## 1. Executive Summary
Falak Pay tracks compliance obligations across **5 regulatory frameworks** (SAMA CSF, PDPL, NCA ECC, PCI-DSS, SWIFT CSP). Across all logged incidents, the **on-time notification rate stands at 40%** — a figure dragged down almost entirely by one finding requiring immediate governance attention: a historical incident that was **not reported to any regulator at the time of discovery**, and was only formally notified approximately **395 days later**, after an internal governance review surfaced it. This is a direct structural replay of the 2016/2017 Uber breach concealment pattern.

Two additional notification clocks are currently live: one within its window, one **already overdue** (SWIFT CSP, configuration drift finding). Six compliance gaps are tracked, three of which cross-reference findings already identified elsewhere in this series (Lab 06, Lab 07, Lab 11) — demonstrating consistency across independent assurance sources, which should accelerate rather than dilute their priority.

## 2. Scope &amp; Methodology
- **Scope:** 5 regulatory frameworks, 4 incidents (8 notification requirements), 6 compliance gaps, 5 regulatory correspondence records
- **Reference case:** Uber, 2016 breach / 2017 disclosure — used as the structural benchmark for notification-timeline compliance failure
- **Tooling:** Regulatory Compliance & Multi-Framework Obligations Tracker (this lab's application)
- **Methodology note:** Each incident is checked against every applicable framework independently — a single incident can be simultaneously compliant with one regulation's deadline and non-compliant with another's, since deadlines range from 2 hours (SAMA CSF) to 72 hours (PDPL, PCI-DSS).

## 3. Key Metrics
| Metric | Value |
|---|---|
| Regulatory frameworks tracked | 5 |
| On-time notification rate | 40% |
| Notifications sent late | 3 |
| Notifications currently overdue (not yet sent) | 1 |
| Open compliance gaps | 5 (of 6 total) |

## 4. Critical Finding — Uber Pattern Replay

### Finding: Historical Payment Data Exposure — Not Reported at Time of Discovery
- **Discovered:** ~400 days before this assessment
- **Notified:** Only ~5 days before this assessment — approximately **395 days after discovery**
- **Frameworks triggered:** SAMA CSF (2-hour deadline — missed by ~395 days), PDPL (72-hour deadline — missed by ~392 days), PCI-DSS (72-hour deadline — missed by ~392 days)
- **What happened:** A third-party backup storage exposure was identified but handled informally rather than through the regulatory notification process, and was only formally reported after an unrelated internal governance review surfaced it.
- **Direct parallel to Uber:** Structurally identical to the 2016/2017 Uber case — a real incident, known internally, not escalated through a tracked regulatory obligation, disclosed only much later and not proactively.
- **Recommendation:** This finding should be treated as the organization's top compliance priority, independent of the underlying technical severity of the original exposure. The concealment/delay pattern itself — not just the data exposure — is what regulators penalize most severely, as the Uber case's $148 million settlement demonstrates.

## 5. Currently Live Notification Clocks
| Incident | Framework | Status | Detail |
|---|---|---|---|
| SWIFT Terminal Configuration Drift Detected | SWIFT CSP | **OVERDUE** | Notification obligation triggered, not yet completed |
| Suspicious Third-Party API Integration Traffic Pattern | PDPL, NCA ECC | Pending — within window | Investigation ongoing, clocks running |

The SWIFT CSP overdue notification requires immediate action — every hour it remains unaddressed compounds the compliance gap.

## 6. Well-Managed Example (for contrast)
**SecurePay Payment Switch Anomalous Access Attempt:** Both applicable notification requirements (SAMA CSF, PCI-DSS) were met on time, following the Escalation Matrix process established in Lab 04 — demonstrating the tracked-obligation model works when actually followed.

## 7. Compliance Gaps Cross-Referenced from Other Assurance Sources
| Gap | Framework | Cross-Reference | Severity |
|---|---|---|---|
| Cloud Security Policy Gap | NCA ECC | Lab 06 / Lab 07 | High |
| Third-Party & M&A Security Integration Policy Still Draft | SAMA CSF | Lab 06 / Lab 11 | Medium |
| Build Infrastructure Access Control Weakness | NCA ECC | Lab 11 | Critical |

These three gaps being independently identified by policy review (Lab 06), cloud posture scanning (Lab 07), and internal audit (Lab 11) is a positive signal about the consistency of Falak Pay's assurance activities — but also means they can no longer be treated as isolated, lower-priority items.

## 8. Recommendations &amp; Roadmap
| Priority | Action | Owner | Target Date |
|---|---|---|---|
| P1 | Complete SWIFT CSP notification for the configuration drift finding | Noura Al-Qahtani | Immediate |
| P1 | Conduct root-cause review of why the historical payment data exposure wasn't notified at time of discovery; implement a mandatory notification-clock-start trigger for every confirmed incident | Khalid Al-Mutairi | Within 1 week |
| P2 | Close the Build Infrastructure Access Control finding (also flagged Critical in Lab 11) | Omar Al-Shammari | Per Lab 11's remediation SLA |
| P2 | Finalize Cloud Security Policy and Third-Party & M&A Security Integration Policy | Khalid Al-Mutairi | Next Committee meeting |
| P3 | Complete overdue PCI-DSS quarterly ASV scan | Fatimah Al-Zahrani | Within 2 weeks |

## 9. Conclusion
Falak Pay's regulatory compliance tracking correctly identifies both live, real-time obligations and — critically — a historical failure to notify that mirrors one of the most consequential compliance failures in recent corporate history. The presence of this tracker is itself the remediation for the underlying pattern: a notification obligation that runs on a tracked, computed clock cannot quietly slip for a year the way it did at Uber.

## 10. Sign-off
| Name | Role | Date |
|---|---|---|
| Khalid Al-Mutairi | CISO | |
| Board Risk &amp; Compliance Committee Chair | | |

---
*This report was generated against the seeded demo dataset in this lab (`seed_demo_data.py`). Regenerate the live version anytime via the app's `/report` view.*
