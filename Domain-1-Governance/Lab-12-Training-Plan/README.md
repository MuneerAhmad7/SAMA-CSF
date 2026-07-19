# Lab 13 — Security Team Training & Certification Plan
**Deepens:** SAMA CSF 1.7 (Cyber Security Training) | NCA ECC 1‑10 (technical staff sub-requirements)

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 13 of N — built around the 2015 OPM breach, where the gap wasn't awareness, it was technical depth.

---

## 0. How this lab relates to Lab 09

Lab 09 built a broad, organization-wide **awareness** program — every employee, phishing/vishing simulations, role-based courses. It's the right tool for "can 500 people recognize a phishing email."

SAMA CSF 1.7 asks a narrower, deeper question that Lab 09 only touched briefly: **is the security team itself technically qualified** — the right certifications, the right depth in the right specialties, a documented needs assessment, not just a training video everyone clicked through. This lab builds that tool specifically: a **skills matrix, certification tracker, and technical training plan for the security function itself**, not the whole company.

## 1. The real-world problem

**Case: U.S. Office of Personnel Management (OPM), breach discovered 2015.**

Between 2014 and 2015, attackers compromised OPM's systems and stole records for over **21 million people**, including highly sensitive background-investigation data — the kind of information collected for security clearances, covering not just federal employees but their family members and associates. It remains one of the most consequential breaches of government data on record.

A subsequent U.S. congressional oversight investigation was unusually direct about the underlying cause: **OPM's own Inspector General had flagged serious weaknesses in the agency's technical security capability for years before the breach**, in audit after audit, and those warnings had not translated into the technical staffing, training, or remediation needed to close the gap. The breach wasn't the result of one novel, unstoppable technique — it was the outcome of a technical capability gap that had been documented and left open.

### Root causes (widely documented in the subsequent congressional report, and exactly what a training/certification plan exists to prevent)
| Root cause | What was missing |
|---|---|
| Repeated audit findings about weak technical security capability, not acted on | A tracked training needs assessment tied directly to identified skill gaps, not a generic annual course |
| No apparent systematic tracking of staff certifications against role requirements | A certification tracker with expiry monitoring — a lapsed or missing credential for a technical role is itself a risk signal |
| Security staff skill depth not matched to the sensitivity of the systems they protected | A skills matrix comparing current competency against the level actually required for the role, by specialty |
| Training treated as a compliance checkbox rather than a funded, planned program | A budgeted, dated training plan with named owners and completion tracking, the same discipline this series applies to vulnerabilities and audit findings |

This is exactly why **SAMA CSF 1.7 requires technical training for security staff, certification requirements, annual training needs assessment, and training records maintenance** — as a distinct, deeper obligation from general staff awareness.

## 2. What this lab builds

A **Security Team Training & Certification Plan Tracker** — Flask + SQLite, same clean custom UI as Labs 03–12 — for **Falak Pay Financial Company**, that:

1. Maintains a **Security Team Roster** — every technical security team member and their role.
2. Runs a **Skills Matrix** — current vs. required competency level (0–4) per person, per specialty (Incident Response, Cloud Security, Digital Forensics, Penetration Testing, GRC/Audit, Secure Code Review), visualized the same way Lab 05 visualizes maturity gaps.
3. Tracks a **Certification Register** with expiry monitoring — Active / Expiring Soon / Expired, flagged automatically.
4. Maintains a **Training Plan** — needs-assessment-driven training items, each with a target skill, budget, target date, and status.
5. Produces a **Dashboard** showing the widest skill gaps, expiring/expired certifications, and training plan completion.
6. Generates a **printable, audit-ready report** (`/report`).

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 1.7 | Technical training for security staff | Training Plan module |
| SAMA CSF 1.7 | Certification requirements (CISSP, CISM, etc.) | Certification Register |
| SAMA CSF 1.7 | Training needs assessment annually | Skills Matrix — current vs. required gap analysis |
| SAMA CSF 1.7 | Training records maintenance | Training Plan — completed items with evidence notes |
| SAMA CSF 1.7 | Specialized training for developers (secure coding) | Skills Matrix — Secure Code Review specialty |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5012
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec training-plan python seed_demo_data.py
```
Seeds 6 security team members, a skills matrix across 6 specialties, certification records (including one already Expired and one Expiring Soon), and a training plan — including a direct replay of the OPM pattern: a Critical skill gap in Digital Forensics that's been flagged in successive assessments without a funded plan to close it, cross-referenced against Lab 11's audit findings.

### Step 1 — Read the case study
Open `docs/case-study-opm-breach.md` first.

### Step 2 — Review the Team Roster
Go to **Team** — note roles and tenure.

### Step 3 — Review the Skills Matrix
Go to **Skills Matrix** — find the widest current-vs-required gap, the OPM-pattern finding.

### Step 4 — Review the Certification Register
Go to **Certifications** — find the Expired and Expiring Soon entries.

### Step 5 — Review the Training Plan
Go to **Training Plan** — see how needs-assessment gaps translate (or don't yet) into funded, dated plan items.

### Step 6 — Add a training plan item to close the OPM-pattern gap
Log a new training plan item targeting the Digital Forensics gap, with budget and a target date.

### Step 7 — Check the Dashboard
Review the widest skill gaps, certification status, and training plan completion.

### Step 8 — Generate the audit-ready report
Go to **`/report`** — print/save as PDF.

### Step 9 — Write the documentation report
Open `report/training-plan-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-13-training-plan/
├── README.md
├── docs/                 ← case study + blank training & certification policy template
├── src/                  ← Training Plan Tracker app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + skills matrix screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Team Roster reviewed
- [ ] Skills Matrix reviewed — OPM-pattern gap identified
- [ ] Certification Register reviewed — expired/expiring flagged
- [ ] Training Plan reviewed
- [ ] New training plan item logged against the identified gap
- [ ] Dashboard reviewed
- [ ] Audit-ready report generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Next lab

**Lab 14 — NCA ECC 3‑1 Incident Response & Forensics**, built around a real-world incident response failure.
