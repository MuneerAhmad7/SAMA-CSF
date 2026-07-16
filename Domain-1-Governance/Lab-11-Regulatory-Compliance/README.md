# Lab 12 — Regulatory Compliance & Multi-Framework Obligations
**Maps to:** SAMA CSF 1.9 (Regulatory Compliance) | NCA ECC 1‑7 (Compliance with Cybersecurity Standards, Laws, and Regulations) | PDPL (SDAIA)

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 12 of N — the final piece of SAMA CSF Domain 1, and arguably the most unforgiving control in this whole series: notification deadlines don't care how good your excuse is.

---

## 1. The real-world problem

**Case: Uber, 2016 breach — disclosed November 2017.**

In late 2016, attackers accessed a third-party cloud storage service used by Uber and obtained personal data for approximately **57 million riders and drivers**, including names, email addresses, phone numbers, and driver's license numbers for about 600,000 drivers. Uber did not report the breach to regulators or notify affected individuals at the time. Instead, the company **paid the attackers to delete the data and stay silent**, and the breach only became public roughly **one year later**, in November 2017, under new company leadership.

The technical intrusion — a third-party service compromise — is almost a footnote in this case. The consequential failure was regulatory: multiple U.S. state attorneys general and the FTC pursued action against Uber specifically over the **concealment and delayed notification**, resulting in a multistate settlement of **$148 million** and an FTC settlement requiring 20 years of independent privacy audits. The individual most directly involved in managing the response was separately prosecuted for obstruction related to concealing the incident from regulators.

### Root causes (widely documented, and exactly what a regulatory compliance program exists to prevent)
| Root cause | What was missing |
|---|---|
| No tracked notification deadline per applicable regulation | A registered obligation, with a computed deadline, for every regulation that could apply to a given incident |
| Decision to conceal made informally, without a compliance function tracking the clock | An independent, systematic notification tracker that doesn't depend on individual judgment calls under pressure |
| A year-long gap between discovery and disclosure | Escalation the moment a notification deadline is at risk of being missed — not a debate about whether to notify at all |
| Regulators discovered the truth after the fact, not from the company | Every notification obligation tracked to completion and verifiable, the same way a Critical vulnerability or audit finding is tracked in this series |

This is exactly why **SAMA CSF 1.9 requires tracked SAMA CSF compliance monitoring and cross-border regulation compliance**, why **NCA ECC 1‑7 requires ongoing compliance monitoring and timely gap remediation**, and why **PDPL imposes a hard 72-hour breach notification requirement to SDAIA** — none of which are satisfied by a policy that says "we will notify appropriately." They require a tracked, time-bound, escalating obligation.

## 2. What this lab builds

A **Regulatory Compliance & Multi-Framework Obligations Tracker** — Flask + SQLite, same clean custom UI as Labs 03–11 — for **Falak Pay Financial Company**, that:

1. Maintains a **Regulatory Framework Register** — every regulation/standard that applies (SAMA CSF, NCA ECC, PDPL, PCI-DSS, SWIFT CSP), each with its own critical-incident notification deadline.
2. Runs an **Incident Notification Tracker** — the core mechanic. Every incident is checked against **every applicable framework simultaneously**, with a computed deadline per framework, and a live On Time / Late / Pending status — because one incident can trigger multiple, different regulatory clocks at once.
3. Tracks a **Compliance Gap Register**, cross-referencing gaps already surfaced elsewhere in this series (Lab 06's policy gaps, Lab 11's audit findings) against the specific regulation each one violates.
4. Logs **Regulatory Correspondence** — every formal exchange with SAMA, NCA, or SDAIA, with its own due date.
5. Produces a **Dashboard** with on-time notification rate, upcoming deadlines, and open compliance gaps by framework.
6. Generates a **printable, audit-ready report** (`/report`).

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 1.9 | SAMA CSF compliance monitoring | Regulatory Framework Register |
| SAMA CSF 5.3 | SAMA notification within 2 hours for critical incidents | Incident Notification Tracker — SAMA CSF framework, 2-hour deadline |
| PDPL | 72-hour breach notification to SDAIA | Incident Notification Tracker — PDPL framework, 72-hour deadline |
| SAMA CSF 1.9 | Cross-border regulation compliance, compliance gap tracking | Compliance Gap Register |
| NCA ECC 1‑7‑2 / 1‑7‑3 | Compliance monitoring, gap remediation | Compliance Gap Register — severity, owner, due date |
| SAMA CSF 1.9 | PCI-DSS / SWIFT CSP compliance (for card processors) | Regulatory Framework Register — PCI-DSS, SWIFT CSP entries |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5011
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec regulatory-compliance python seed_demo_data.py
```
Seeds 5 regulatory frameworks, 4 incidents, notification tracking across every applicable framework per incident (including a direct replay of the Uber pattern: an incident discovered, concealed, and notified roughly a year late against both a 2-hour and a 72-hour deadline), 6 compliance gaps, and 5 regulatory correspondence records.

### Step 1 — Read the case study
Open `docs/case-study-uber-breach.md` first.

### Step 2 — Review the Regulatory Framework Register
Go to **Frameworks** — note each regulation's specific notification deadline.

### Step 3 — Review the Incident Notification Tracker
Go to **Notifications** — find the Uber-replay incident and see how badly it missed both applicable deadlines, expressed in days rather than hours.

### Step 4 — Review the Compliance Gap Register
Go to **Compliance Gaps** — note gaps cross-referenced from earlier labs, now mapped to the specific regulation they violate.

### Step 5 — Review Regulatory Correspondence
Go to **Correspondence** — check for any overdue response to a regulator inquiry.

### Step 6 — Check the Dashboard
Review on-time notification rate, upcoming deadlines, and open gaps by framework.

### Step 7 — Generate the audit-ready report
Go to **`/report`** — print/save as PDF.

### Step 8 — Write the documentation report
Open `report/regulatory-compliance-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-12-regulatory-compliance/
├── README.md
├── docs/                 ← case study + blank regulatory compliance policy template
├── src/                  ← Regulatory Compliance Tracker app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + notification tracker screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Regulatory Framework Register reviewed — deadlines understood
- [ ] Uber-replay incident identified in the Notification Tracker
- [ ] Compliance Gap Register reviewed, cross-references to earlier labs noted
- [ ] Regulatory Correspondence reviewed for overdue items
- [ ] Dashboard reviewed
- [ ] Audit-ready report generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Series status — SAMA CSF Domain 1 complete

| Sub-domain | Lab |
|---|---|
| 1.1 Governance Structure | Lab 01, Lab 04 |
| 1.2 Strategy | Lab 05 |
| 1.3 Policy | Lab 01, Lab 06 |
| 1.4 Roles & Responsibilities | Lab 01, Lab 04 |
| 1.5 Security in Project Management | Lab 08 |
| 1.6 / 1.7 Awareness & Training | Lab 09 |
| 1.8 Review and Audit | Lab 11 |
| 1.9 Regulatory Compliance | **Lab 12 (this lab)** |

## 9. Next lab

**Lab 13 — NCA ECC 3‑1 Incident Response & Forensics**, built around a real-world incident response failure.
