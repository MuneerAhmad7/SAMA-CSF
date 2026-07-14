# Lab 08 — Security in Project Management & the SDLC
**Maps to:** SAMA CSF 1.5 (Cyber Security in Project Management), 3.2 (Application Security) | NCA ECC 1‑6 (Cybersecurity in IT Projects), 2‑8 (Secure Software Development)

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 8 of N — built around the 2018 British Airways Magecart breach, the textbook case of a change that reached production without a real security gate.

---

## 1. The real-world problem

**Case: British Airways, disclosed September 2018.**

Attackers compromised British Airways' website and mobile app by injecting malicious JavaScript — a technique now widely known as **"Magecart"** — into the payment checkout page. The injected script silently captured payment card details (including CVV numbers) as customers typed them, sending a copy to a server controlled by the attackers, while the transaction itself completed normally. The compromise ran for roughly **two and a half weeks** before discovery, exposing personal and payment data for approximately **380,000 customers**. The UK's Information Commissioner's Office (ICO) issued what was, at the time, one of the largest data protection fines under GDPR.

The technical mechanism — a single altered or malicious script running on a payment page — is almost beside the point. The real story is **what should have stopped that script from ever reaching production, or from running unnoticed for over two weeks once it did.**

### Root causes (widely discussed in public post-incident analysis, and exactly what project/SDLC security controls exist to prevent)
| Root cause | What was missing |
|---|---|
| A code change reached the live payment page without a rigorous security review gate | Documented security sign-off required before any change to a Critical/customer-facing project goes live |
| No integrity control on scripts running on the payment page | A code/script integrity register — knowing exactly what's supposed to be running, and detecting anything that isn't |
| The malicious script ran for over two weeks before detection | Continuous monitoring for unauthorized changes to customer-facing, especially payment-related, pages |
| No apparent threat modeling specific to the payment flow's unique risk | Security requirements defined at project initiation, not bolted on afterward |

This is exactly why **SAMA CSF 1.5 requires security sign-off before go-live and security gate reviews at each project phase**, and why **NCA ECC 2‑8 requires secure coding standards, code review, and environment separation** as non-negotiable steps in any software delivery process — not optional steps that can be skipped under deadline pressure.

## 2. What this lab builds

A **Project Security Gate Tracker** — Flask + SQLite, same clean custom UI as Labs 03–07 — for **Falak Pay Financial Company**, that:

1. Maintains a **Project Register** — every active/completed project, tagged by criticality and business unit.
2. Tracks a **Security Gate Checklist** per project across six phases (Initiation → Design → Build → Test → Deploy → Post-Implementation), each requiring a named approver and evidence before it can be marked Passed.
3. Maintains a **Third-Party Script / Code Integrity Register** — exactly the control that was missing at British Airways — tracking every script running on customer-facing pages, whether it has Subresource Integrity (SRI) pinned, and when it was last reviewed.
4. Logs a **Change Record** for every production deployment, flagging any change that went live **without** its Deploy gate having Passed — the precise failure mode behind the BA breach.
5. Produces a **Dashboard** showing gate compliance, flagged ungated changes, and unprotected third-party scripts on sensitive pages.
6. Generates a **printable, audit-ready report** (`/report`).

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 1.5 / ECC 1‑6‑2 | Security requirements defined for each project | Project Register + Initiation gate |
| SAMA CSF 1.5 / ECC 1‑6‑3 | Security review gates at each project phase | Security Gate Checklist — 6 phases |
| SAMA CSF 1.5 / ECC 1‑6‑4 | Security testing before deployment | Test gate (SAST/DAST/pentest evidence) |
| SAMA CSF 1.5 / ECC 1‑6‑5 | Security sign-off before go-live | Deploy gate — named approver required |
| SAMA CSF 3.2 / ECC 2‑8‑4 | Code review, secure coding standards | Build gate |
| NCA ECC 2‑8‑6 | Environment separation, controlled deployment | Change Record — flags ungated changes |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5007
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec project-security python seed_demo_data.py
```
Seeds 6 realistic Falak Pay projects with gate checklists across all phases, 8 third-party scripts (including one on the payment page with no SRI pinned — a direct BA replay), and change records — including one deployment that went live without its Deploy gate passing.

### Step 1 — Read the case study
Open `docs/case-study-british-airways-breach.md` first.

### Step 2 — Review the Project Register
Go to **Projects** — note criticality and current phase for each.

### Step 3 — Review a project's Security Gate Checklist
Pick the "Payment Checkout Redesign" project — walk through its six gates and find where the process broke down.

### Step 4 — Review the Third-Party Script Register
Go to **Scripts** — find the payment-page script with no SRI hash pinned. This is the exact control gap behind the BA breach.

### Step 5 — Review the Change Log
Go to **Changes** — find the change flagged as deployed without a passed Deploy gate.

### Step 6 — Work a gate to Passed
Pick an In Progress gate, add an approver and evidence notes, and mark it Passed — watch the audit log and dashboard update.

### Step 7 — Check the Dashboard
Review overall gate compliance %, flagged ungated changes, and unprotected scripts.

### Step 8 — Generate the audit-ready report
Go to **`/report`** — print/save as PDF.

### Step 9 — Write the documentation report
Open `report/project-security-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-08-project-security/
├── README.md
├── docs/                 ← case study + blank project security policy template
├── src/                  ← Project Security Gate Tracker app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + gate checklist screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Project Register reviewed
- [ ] Security Gate Checklist reviewed on at least one project end to end
- [ ] Third-party script gap identified in the Script Register
- [ ] Ungated change identified in the Change Log
- [ ] One gate walked through to Passed status
- [ ] Dashboard reviewed
- [ ] Audit-ready report generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Next lab

**Lab 09 — NCA ECC 3‑1 Incident Response & Forensics**, built around a real-world incident response failure.
