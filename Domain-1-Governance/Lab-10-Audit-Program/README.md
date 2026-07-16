# Lab 11 — Cyber Security Review & Audit
**Maps to:** SAMA CSF 1.8 (Cyber Security Review and Audit) | NCA ECC 1‑8 (Periodic Cybersecurity Review and Audit)

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 11 of N — the last uncovered piece of SAMA CSF Domain 1, built around the 2020 SolarWinds breach: what happens when a known finding never gets tracked to closure.

---

## 1. The real-world problem

**Case: SolarWinds, disclosed December 2020.**

Attackers compromised SolarWinds' software build pipeline and inserted malicious code (later named "Sunburst") into updates for its Orion IT management platform, which were then distributed to roughly 18,000 customers, including U.S. government agencies and Fortune 500 companies — one of the most consequential supply-chain attacks ever discovered.

What makes this case relevant to an **audit and review** lab specifically: subsequent public reporting, including U.S. congressional testimony, surfaced that **security weaknesses at SolarWinds — including weak password practices on infrastructure supporting software builds — had reportedly been flagged in earlier internal security assessments, years before the breach was discovered.** A security researcher had also separately warned the company about an exposed update server with a weak, easily-guessed password. The technical compromise itself is well documented; the governance failure sitting underneath it is what this lab targets: **a known weakness, identified through a review process, that did not get tracked to verified remediation before it became the entry point for a major breach.**

### Root causes (widely discussed in public post-incident analysis, and exactly what a mature audit program exists to prevent)
| Root cause | What was missing |
|---|---|
| Known weaknesses identified in earlier reviews, not remediated | A tracked findings register with severity-based remediation SLAs, not a report that gets filed and forgotten |
| No visible escalation when findings aged past their remediation deadline | Overdue-finding alerting to leadership/Audit Committee, the same discipline this series already applies to vulnerabilities (Lab 03) |
| Findings on build/release infrastructure weren't treated with the urgency their potential blast radius warranted | Severity and business-impact-based prioritization, not just chronological queue order |
| No apparent pattern-recognition across review cycles | Repeat-finding tracking — the same weakness surfacing across multiple audits is itself a signal that remediation isn't sticking |

This is exactly why **SAMA CSF 1.8 requires annual internal review, independent external assessment, and — critically — remediation tracking and reporting**, and why **NCA ECC 1‑8 requires audit findings to be reported to management**, not just to the audit file.

## 2. What this lab builds

A **Cyber Security Audit & Assurance Tracker** — Flask + SQLite, same clean custom UI as Labs 03–10 — for **Falak Pay Financial Company**, that:

1. Maintains an **Audit Engagement Register** — every internal audit, external audit, penetration test, and regulatory examination, with scope and status.
2. Tracks a **Findings Register** with **severity-based remediation SLAs** (auto-computed, overdue findings flagged red — the same discipline Lab 03 applies to vulnerabilities, applied here to audit findings).
3. Flags **Repeat Findings** — the same weakness identified across multiple engagements, the exact pattern behind the SolarWinds case.
4. Logs **Audit Committee Reporting** — because a finding that never reaches a committee agenda might as well not exist for governance purposes.
5. Produces a **Dashboard** with remediation compliance %, overdue findings, and repeat-finding alerts.
6. Generates a **printable, board-ready report** (`/report`).

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 1.8 | Annual internal cybersecurity audit | Audit Engagement Register — Internal Audit type |
| SAMA CSF 1.8 | Independent external assessment (annually) | Audit Engagement Register — External Audit type |
| SAMA CSF 1.8 | Penetration testing (annual minimum) | Audit Engagement Register — Penetration Test type |
| SAMA CSF 1.8 | Remediation tracking and reporting | Findings Register — severity-based SLA, status workflow |
| NCA ECC 1‑8‑5 / 1‑8‑6 | Remediation tracking, audit findings reported to management | Committee Reporting Log |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5010
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec audit-assurance python seed_demo_data.py
```
Seeds 5 audit engagements (internal, external, pentest, regulatory) and 14 findings, including a direct replay of the SolarWinds pattern: a Critical finding on build/release infrastructure access controls, identified in an earlier internal review, left unremediated well past its SLA, and flagged again as a **repeat finding** in a later engagement.

### Step 1 — Read the case study
Open `docs/case-study-solarwinds-breach.md` first.

### Step 2 — Review the Audit Engagement Register
Go to **Engagements** — note the mix of internal, external, and pentest coverage.

### Step 3 — Review the Findings Register
Go to **Findings** — find the SolarWinds-replay finding: Critical, overdue, and flagged as a repeat finding from an earlier engagement.

### Step 4 — Work a finding to closure
Pick an overdue finding, move it through In Progress → Remediated → Verified Closed, with owner and evidence notes.

### Step 5 — Log a Committee report
Go to **Committee Reports** — log a report cycle referencing the overdue/repeat findings that should be escalated.

### Step 6 — Check the Dashboard
Review remediation compliance %, overdue findings, and repeat-finding alerts.

### Step 7 — Generate the board-ready report
Go to **`/report`** — print/save as PDF.

### Step 8 — Write the documentation report
Open `report/audit-assurance-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-11-audit-assurance/
├── README.md
├── docs/                 ← case study + blank audit & review policy template
├── src/                  ← Audit & Assurance Tracker app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + findings register screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Audit Engagement Register reviewed
- [ ] SolarWinds-replay finding identified — Critical, overdue, repeat
- [ ] One overdue finding walked through to Verified Closed
- [ ] Committee report logged
- [ ] Dashboard reviewed
- [ ] Board-ready report generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Series status

This lab completes SAMA CSF Domain 1 (Leadership & Governance) coverage across the series:

| Sub-domain | Lab |
|---|---|
| 1.1 Governance Structure | Lab 01, Lab 04 |
| 1.2 Strategy | Lab 05 |
| 1.3 Policy | Lab 01, Lab 06 |
| 1.4 Roles & Responsibilities | Lab 01, Lab 04 |
| 1.5 Security in Project Management | Lab 08 |
| 1.6 / 1.7 Awareness & Training | Lab 09 |
| 1.8 Review and Audit | **Lab 11 (this lab)** |
| 1.9 Regulatory Compliance | Threaded through every lab's control mapping |

## 9. Next lab

**Lab 12 — NCA ECC 3‑1 Incident Response & Forensics**, built around a real-world incident response failure.
