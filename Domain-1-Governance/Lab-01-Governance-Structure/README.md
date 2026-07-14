# Lab 01 — Cybersecurity Governance & Leadership
**Maps to:** SAMA CSF Domain 1 (Leadership & Governance, controls 1.1–1.9) | NCA ECC Domain 1 (Cybersecurity Governance, 1‑1 to 1‑10) | ISO 27001 A.5/A.6

> Series: *90 Days of Saudi Cybersecurity Compliance Labs*
> Lab 1 of N — this one sets the template folder structure and workflow for every lab that follows.

---

## 1. Why this lab exists

Every regulator in KSA (SAMA, NCA, SDAIA) starts an audit the same way: **"Show me your governance structure, your policy, and your evidence that the Board actually saw this."** Most orgs fail Domain 1 not because they lack controls, but because they lack *documented, trackable evidence* of governance activity.

This lab builds a small, real, self-hosted **Governance & Compliance Tracker** that a GRC analyst would actually use to run Domain 1 day-to-day, plus the document templates a real audit would ask for.

## 2. Scenario

You are the newly appointed **Information Security Governance Lead** at a fictional SAMA-regulated fintech, "Falak Pay." You have 90 days to stand up a defensible Cybersecurity Governance program before the next SAMA CSF self-assessment. Today is day 1: governance structure, policy, RACI, and Board reporting.

## 3. Regulatory requirements covered

| Control | Requirement | Where it's implemented in this lab |
|---|---|---|
| SAMA CSF 1.1 / ECC 1‑2 | CISO appointed, reports to Board/CEO, independent from IT | `docs/governance-charter-template.md` |
| SAMA CSF 1.2 / ECC 1‑1 | 3–5 yr strategy, annual review, Board approval | `docs/governance-charter-template.md` |
| SAMA CSF 1.3 / ECC 1‑3 | Board-approved policy, supporting policies, acknowledgment tracking | `docs/cybersecurity-policy-template.md` + tracker `Policies` module |
| SAMA CSF 1.4 / ECC 1‑4 | RACI matrix, segregation of duties | `docs/raci-matrix-template.md` + tracker `RACI` module |
| SAMA CSF 1.1 / ECC 1‑2‑4 | Cyber Security Committee, quarterly Board reporting | `docs/board-reporting-template.md` + tracker `Board Reports` module |
| SAMA CSF 1.2 | KPIs/KRIs defined and monitored | tracker `KPI/KRI` module |
| SAMA CSF 1.9 / ECC 1‑7 | Regulatory compliance tracking | tracker `Compliance Checklist` module (pre-seeded with all Domain 1 controls) |

## 4. Environment (free/local — Docker)

```
Requirements: Docker + Docker Compose only. No cloud account needed.
```

```bash
cd src
docker compose up --build
# App available at http://localhost:5000
```

The stack is intentionally simple: **Flask + SQLite**, one container, no external dependencies — so it runs identically on any laptop or a free-tier VM, and is easy to read/extend for your GitHub readers.

## 5. Step-by-step workflow

### Step 1 — Stand up the governance structure
1. Open `docs/governance-charter-template.md`, fill in your fictional org's names (CISO, Committee members, reporting line).
2. In the tracker, go to **RACI** and enter the roles from the charter (Step is pre-seeded with a sample RACI — edit it).

### Step 2 — Publish the policy
1. Open `docs/cybersecurity-policy-template.md`, customize section 4 (scope) and section 9 (roles).
2. In the tracker → **Policies**, create a record: title, owner, status `Draft` → `Under Review` → `Approved` → `Published`, set `review_date` = today + 365 days.
3. This models the real lifecycle SAMA/NCA auditors ask to see evidence of.

### Step 3 — Run a (simulated) governance committee meeting
1. Open `docs/board-reporting-template.md`.
2. In the tracker → **Meetings**, log a Q1 Cyber Security Committee meeting: attendees, agenda, decisions, action items with owners/due dates.

### Step 4 — Define and track KPIs/KRIs
1. In the tracker → **KPI/KRI**, add at least 5 metrics regulators expect to see, e.g.:
   - % systems patched within SLA
   - # phishing simulation click-rate
   - # overdue risk treatment plans
   - Mean time to detect (MTTD) / respond (MTTR)
   - % staff completed annual awareness training
2. Set a `target`, an `actual`, and let the dashboard compute status (Green/Amber/Red).

### Step 5 — Self-assess against the control checklist
1. Tracker → **Compliance Checklist** is pre-seeded with every SAMA CSF 1.1–1.9 and NCA ECC 1‑1→1‑10 control from the framework.
2. Mark each `Implemented / Partial / Not Implemented`, attach an evidence note (e.g., "see policy v1.2, approved 2026‑07‑01").
3. Dashboard home page shows your live compliance %.

### Step 6 — Produce the audit-ready report
1. Copy `report/governance-assessment-report-template.md`, fill it in using the data now sitting in your tracker.
2. This is the artifact you'd actually hand to an internal auditor or SAMA examiner.

## 6. What to commit to GitHub

```
lab-01-sama-csf-governance/
├── README.md                     ← this file
├── docs/                         ← filled-in templates (your evidence)
├── src/                          ← the tracker app (Flask + SQLite + Docker)
├── report/                       ← your completed assessment report
└── screenshots/                  ← dashboard screenshots (add your own)
```

Suggested commit message: `Lab 01: SAMA CSF / NCA ECC Domain 1 - Governance program + GRC tracker`

## 7. What "done" looks like

- [ ] Governance charter filled in and committed
- [ ] Policy created and moved through full lifecycle in tracker
- [ ] RACI matrix populated for at least 8 governance activities
- [ ] One committee meeting logged with ≥3 action items
- [ ] 5+ KPIs/KRIs tracked with RAG status
- [ ] Compliance checklist scored (all 19 Domain-1 controls)
- [ ] Assessment report exported and committed
- [ ] Dashboard screenshot added
- [ ] LinkedIn post published (see `linkedin-post-draft.md`)

## 8. Next lab

**Lab 02 — NCA ECC Domain 2, Subdomain 2‑2: Identity & Access Management** (MFA, PAM, access reviews) — hands-on with a local Keycloak/OpenLDAP stack.
