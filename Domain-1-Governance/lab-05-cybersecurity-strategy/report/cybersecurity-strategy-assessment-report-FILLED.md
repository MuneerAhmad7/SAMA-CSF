# Cybersecurity Strategy Assessment Report
**Organization:** Falak Pay Financial Company (fictional entity, lab use)
**Strategic Period:** 2026–2029 | **Assessment Date:** *[generated from seeded demo data]*
**Maps to:** SAMA CSF 1.2, NCA ECC 1‑1 | **Classification:** Confidential — Internal Use Only

---

## 1. Executive Summary
Falak Pay's Cybersecurity Strategy document is **100% complete** across all required elements (vision, business alignment, threat landscape, budget, governance). Average maturity across 10 domains stands at **2.3 (current) against a 3.7 (target)** — a gap of 1.4 levels, consistent with an organization roughly 18 months into a multi-year strategic uplift.

Of 14 roadmap initiatives, **4 are complete (28.6%)**, concentrated in the Foundation phase. Budget utilization stands at **24.4%** of allocated funds. One initiative — Annual DR Test Program Formalization — is **Delayed**, and should be the immediate focus of the next Cyber Security Committee meeting.

The Threat Landscape Register identifies **4 High-risk threats** (score ≥ 6), including a Nation-State/Geopolitical entry — a category explicitly added in direct response to lessons from the 2014 Sony Pictures breach, where a foreseeable geopolitical trigger was not reflected in defensive posture.

## 2. Scope & Methodology
- **Scope:** Enterprise-wide cybersecurity strategy, 10 maturity domains, full threat landscape, 4-phase roadmap
- **Reference case:** Sony Pictures Entertainment, 2014 — used as the structural benchmark for sustained strategic investment
- **Tooling:** Cybersecurity Strategy Builder (this lab's application)

## 3. Key Metrics
| Metric | Value |
|---|---|
| Strategy document completeness | 100% |
| Average maturity (current / target) | 2.3 / 3.7 |
| Roadmap completion | 28.6% (4/14) |
| Delayed initiatives | 1 |
| Budget utilization | 24.4% (SAR 1,520,000 / SAR 18,500,000 total strategy budget) |
| High-risk threats tracked | 4 |

## 4. Widest Maturity Gaps (strategic priorities)
| Domain | Current | Target | Gap |
|---|---|---|---|
| Third-Party & Cloud Security | 1 | 3 | 2 |
| Risk Management | 2 | 4 | 2 |
| Network & Infrastructure Security | 2 | 4 | 2 |
| Data Protection | 2 | 4 | 2 |

**Third-Party & Cloud Security** is both the lowest-scoring domain and tied for the widest gap — consistent with it being the last domain to receive dedicated roadmap investment (Advanced Controls phase, not yet started). This should be reviewed for possible re-prioritization into the Core Controls phase.

## 5. Threat Landscape Highlights
| Threat | Likelihood | Impact | Risk Score |
|---|---|---|---|
| Organized Financial Fraud | High | High | 9 |
| Nation-State / Geopolitical | Medium | High | 6 |
| Ransomware | Medium | High | 6 |
| Unpatched Known Vulnerabilities | Medium | High | 6 |

The Nation-State/Geopolitical entry is deliberately tracked as a standing category, not an ad-hoc addition — this is the specific strategic discipline that was reportedly missing at Sony Pictures ahead of a foreseeable, business-specific geopolitical trigger.

## 6. Roadmap Status by Phase
| Phase | Initiatives | Completed | Progress |
|---|---|---|---|
| Foundation | 4 | 4 | 100% |
| Core Controls | 5 | 0 | 0% (3 In Progress, 1 Delayed, 1 Not Started) |
| Advanced Controls | 4 | 0 | 0% (1 In Progress, 3 Not Started) |
| Optimization | 1 | 0 | 0% (Not Started) |

Foundation phase is fully complete, which is appropriate for an 18-month-old strategy. Core Controls phase progress should be the primary focus of the next two quarters.

## 7. Recommendations & Roadmap
| Priority | Action | Owner | Target Date |
|---|---|---|---|
| P1 | Investigate and resolve delay on Annual DR Test Program Formalization | Omar Al-Shammari | Next Committee meeting |
| P2 | Consider moving Cloud Security Posture Management (CSPM) into Core Controls given Third-Party & Cloud Security's low maturity score | Khalid Al-Mutairi | Next strategy review |
| P2 | Increase budget utilization pace on Data Classification & DLP Rollout (0% spent, Core Controls phase) | Fatimah Al-Zahrani | Q3 2026 |
| P3 | Formally document how the Nation-State/Geopolitical threat category informs specific control decisions, not just the register entry | Khalid Al-Mutairi | Next Charter/Strategy review |

## 8. Conclusion
Falak Pay's Cybersecurity Strategy reflects the core lesson of the Sony Pictures case: security investment is documented, funded, phased, and tied to a living threat landscape rather than treated reactively. The Foundation phase is fully delivered. The primary risk to the strategy's success is pace in the Core Controls phase, particularly around Third-Party & Cloud Security, which remains the organization's least mature domain.

## 9. Sign-off
| Name | Role | Date |
|---|---|---|
| Khalid Al-Mutairi | CISO | |
| Board Risk & Compliance Committee Chair | | |

---
*This report was generated against the seeded demo dataset in this lab (`seed_demo_data.py`). Regenerate the live version anytime via the app's `/report` view.*
