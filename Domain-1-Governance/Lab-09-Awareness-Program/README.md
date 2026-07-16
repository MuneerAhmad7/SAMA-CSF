# Lab 09 — Security Awareness & Training Program
**Maps to:** SAMA CSF 1.6 (Cyber Security Awareness), 1.7 (Cyber Security Training) | NCA ECC 1‑10 (Cybersecurity Awareness and Training)

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 9 of N — built around the 2020 Twitter breach, the case that proved awareness training has to cover the phone, not just the inbox.

---

## 1. The real-world problem

**Case: Twitter, July 2020.**

Attackers ran a **phone-based social engineering (vishing) campaign** targeting Twitter employees, impersonating IT support staff and convincing some employees to provide credentials or approve access through an internal support tool. Using that access, the attackers compromised **dozens of high-profile verified accounts** — including political figures, celebrities, and major companies — and used them to promote a cryptocurrency scam. The incident forced Twitter to temporarily lock all verified accounts from tweeting while it investigated.

The technical access method — an internal admin/support tool — wasn't the real point of failure. **The point of failure was that employees, under social pressure over the phone, provided the access an attacker convincingly impersonating IT support asked for.** Most security awareness programs at the time (and many still today) focus almost entirely on email phishing, leaving phone-based social engineering — vishing — comparatively untested and unaddressed.

### Root causes (widely discussed in public post-incident analysis, and exactly what a mature awareness program exists to prevent)
| Root cause | What was missing |
|---|---|
| Employees successfully socially engineered over the phone | Awareness training and simulation covering vishing specifically, not just email phishing |
| No apparent verification procedure for "IT support" requests for credential/access changes | A documented, trained-on process for verifying identity before granting access changes, regardless of channel |
| Privileged/support-tool access wasn't specially hardened against social engineering | Role-based awareness training for employees with privileged or sensitive tool access |
| No indication of a broad, tested organizational muscle memory for "hang up and verify" | Regular phone-based social engineering simulations, not just email phishing simulations |

This is exactly why **SAMA CSF 1.6 requires role-based awareness for specific groups and quarterly phishing simulation exercises (not limited to email)**, and why **NCA ECC 1‑10 requires new-employee security induction and measured, tracked effectiveness of awareness activities** — not a once-a-year slide deck everyone clicks through.

## 2. What this lab builds

A **Security Awareness & Training Program Tracker** — Flask + SQLite, same clean custom UI as Labs 03–08 — for **Falak Pay Financial Company**, that:

1. Maintains an **Employee Roster** with department, role, and a privileged-access flag (mirroring the Twitter employees with access to sensitive internal tools).
2. Tracks a **Training Catalog** — role-based courses (including a dedicated Vishing & Social Engineering Awareness course) with per-employee assignment, due dates, and completion status.
3. Runs **Simulation Campaigns** across multiple channels — email phishing *and* vishing — with per-employee outcomes (Reported / Clicked-No Data / Clicked-Credentials Given / No Action).
4. Automatically flags **repeat offenders** — employees who failed more than one simulation — and specifically flags **privileged employees who failed a vishing simulation**, the exact risk profile behind the Twitter breach.
5. Produces a **Dashboard** with training completion %, simulation failure rates by channel, and a prioritized follow-up list.
6. Generates a **printable, audit-ready report** (`/report`).

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 1.6 | Annual awareness program for all employees | Training Catalog + Assignment tracking |
| SAMA CSF 1.6 | Role-based awareness for specific groups | Course `audience` field (All Staff / Payments Ops / IT & Admins / Developers / Executives) |
| SAMA CSF 1.6 | Phishing simulation exercises (quarterly minimum) | Simulation Campaigns — Email Phishing type |
| SAMA CSF 1.6 | New joiner security induction | "New Hire Security Induction" course, assigned at hire |
| SAMA CSF 1.6 | Awareness effectiveness measurement | Dashboard — completion %, simulation failure rates, repeat-offender tracking |
| NCA ECC 1‑10‑4 | Phishing exercises | Simulation Campaigns — Vishing type (the Twitter-specific gap) |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5008
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec awareness python seed_demo_data.py
```
Seeds 12 employees across departments (including privileged/IT roles), 8 training courses, training assignments with realistic completion status, and 3 simulation campaigns (2 email phishing, 1 vishing) with per-employee outcomes — including a direct replay of the Twitter risk profile: a privileged employee who provided credentials during the simulated vishing call.

### Step 1 — Read the case study
Open `docs/case-study-twitter-breach.md` first.

### Step 2 — Review the Employee Roster
Go to **Employees** — note who's flagged as privileged.

### Step 3 — Review the Training Catalog and completion status
Go to **Training** — check completion status per employee, and find any overdue assignments.

### Step 4 — Review the Simulation Campaigns
Go to **Simulations** — review the vishing campaign specifically, and find the privileged employee who provided credentials.

### Step 5 — Check the Dashboard
Review overall training completion %, simulation failure rates, and the repeat-offender/high-risk follow-up list.

### Step 6 — Assign follow-up training
Update a flagged employee's Vishing & Social Engineering Awareness course status to reflect mandatory retraining.

### Step 7 — Generate the audit-ready report
Go to **`/report`** — print/save as PDF.

### Step 8 — Write the documentation report
Open `report/awareness-program-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-09-awareness-program/
├── README.md
├── docs/                 ← case study + blank awareness policy template
├── src/                  ← Awareness Program Tracker app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + simulation results screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Employee roster reviewed, privileged employees identified
- [ ] Training completion reviewed, overdue assignments found
- [ ] Vishing simulation results reviewed — Twitter-replay finding identified
- [ ] Dashboard reviewed — repeat offenders and high-risk follow-ups checked
- [ ] Follow-up training assigned to at least one flagged employee
- [ ] Audit-ready report generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Next lab

**Lab 10 — NCA ECC 3‑1 Incident Response & Forensics**, built around a real-world incident response failure.
