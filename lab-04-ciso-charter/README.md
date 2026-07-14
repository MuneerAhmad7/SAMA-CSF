# Lab 04 — CISO Charter, Authority & Independence
**Maps to:** SAMA CSF 1.1 (Governance Structure), 1.2 (Strategy) | NCA ECC 1‑2 (Cybersecurity Management), 1‑4 (Roles & Responsibilities) | ISO 27001 A.5.1, A.6.1.1

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 4 of N — this one is about the document that everything else in this series assumes already exists: a CISO Charter with real teeth.

---

## 1. The real-world problem

**Case: Target Corporation, 2013.**

In November–December 2013, attackers stole payment card and personal data for roughly **40 million credit/debit card accounts and 70 million customer records** from Target, one of the largest retail breaches in U.S. history at the time.

The technical intrusion path is well documented — stolen credentials from a third-party HVAC vendor, lateral movement into the point-of-sale network. But the detail most relevant to this lab is organizational: Target's security monitoring team (using a commercial threat-detection platform monitored partly through a third-party security operations center) **did receive alerts about the malicious activity before the breach became public** — and the alerts did not result in a decisive, empowered response in time to stop the exfiltration.

Target did **not have a dedicated, empowered Chief Information Security Officer role** with direct executive/board access before the breach. In its aftermath, Target's public remediation commitments explicitly included **creating a CISO position with a direct reporting line to executive leadership** — because the absence of that role, with real authority, was identified as a structural gap.

### Root causes (publicly documented, and exactly what a proper CISO Charter exists to prevent)
| Root cause | What was missing |
|---|---|
| Security alerts generated but not decisively actioned | No single accountable executive with clear authority to mobilize a response |
| No dedicated CISO role with board/executive access | Security embedded under IT, without independent escalation power |
| Unclear ownership of "who can pull the trigger" on a security response | No documented, board-approved escalation authority |
| Post-breach, the organization had to build this structure reactively | No charter defining the role, authority, and independence *before* it was needed |

This is exactly why **SAMA CSF 1.1 and NCA ECC 1‑2‑6 mandate that the cybersecurity function be organizationally independent from IT**, why the **CISO must have a defined, direct reporting line**, and why a **documented Charter — not a job description buried in HR — is what regulators expect to see.**

## 2. What this lab builds

A **CISO Charter Builder & Authority Assessment** tool — Flask + SQLite, with the same clean custom UI style as Lab 03 — for **Falak Pay Financial Company**, that:

1. Builds a complete, structured **CISO Charter document** (mandate, authority, independence, budget, escalation rights, reporting lines) through a simple form-based interface — no more editing raw Markdown by hand.
2. Runs a **CISO Authority & Independence Self-Assessment** — 14 controls modeled directly on what Target lacked in 2013, scored against SAMA CSF 1.1/1.2 and NCA ECC 1‑2.
3. Maintains a **governance RACI matrix** and an **escalation matrix** (who gets notified, how fast, at what severity) as living, structured data instead of static tables nobody updates.
4. Produces a **dashboard** showing charter completeness % and authority/independence maturity score.
5. Generates a **printable, board-ready Charter document** (`/report`) you could hand directly to a Board Risk Committee for approval.

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 1.1 / ECC 1‑2‑6 | CISO independent from IT | Authority Assessment control #1 |
| SAMA CSF 1.1 / ECC 1‑2‑2 | CISO appointed with appropriate authority | Charter Builder — Mandate & Authority section |
| SAMA CSF 1.1 | CISO reports to Board/CEO | Charter Builder — Reporting Line field + Authority Assessment |
| SAMA CSF 1.1 | Cyber Security Committee at Board level | Charter Builder — Governance Structure section |
| SAMA CSF 1.2 | Budget allocation for cybersecurity | Authority Assessment — Budget Authority control |
| SAMA CSF 1.4 / ECC 1‑4‑3 | RACI, segregation of duties | RACI module |
| SAMA CSF 5.1 | Escalation procedures | Escalation Matrix module |
| NCA ECC 1‑2‑5 | Adequate resources (budget, personnel, tools) | Authority Assessment |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5003
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec ciso-charter python seed_demo_data.py
```
Seeds a complete, filled CISO Charter for Falak Pay (CISO: Khalid Al-Mutairi), a 14-control authority assessment (all scored), 8 RACI entries, and 6 escalation rules.

### Step 1 — Read the case study
Open `docs/case-study-target-breach.md` first.

### Step 2 — Build (or review) the Charter
Go to **Charter Builder** — walk through each section: Mandate, Reporting Line, Independence, Budget Authority, Governance Structure, Term & Review. If you loaded demo data, review and edit as if you were updating it for a real annual review.

### Step 3 — Run the Authority & Independence Assessment
Go to **Authority Assessment** — 14 controls, each modeled on a specific Target-2013 gap (e.g., "Is the CISO organizationally separate from IT?", "Can the CISO escalate directly to the Board without IT sign-off?"). Score each Met/Partial/Not Met with evidence.

### Step 4 — Review RACI and Escalation
Go to **RACI** and **Escalation Matrix** — confirm accountability is clear for every major governance activity, and that escalation timeframes are defined (not "someone will probably notice").

### Step 5 — Check the Dashboard
Review your Charter completeness % and Authority/Independence maturity score.

### Step 6 — Generate the board-ready document
Go to **`/report`** — print/save as PDF. This is the actual artifact you'd submit for Board approval.

### Step 7 — Write up the documentation
Open `report/ciso-charter-assessment-report-FILLED.md` — a completed example assessment report referencing the Target case, ready to adapt.

## 6. What to commit to GitHub

```
lab-04-ciso-charter/
├── README.md
├── docs/                 ← case study + filled + blank charter templates
├── src/                  ← Charter Builder app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + printable charter screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Charter reviewed/edited section by section
- [ ] Authority Assessment scored (14 controls)
- [ ] RACI and Escalation Matrix reviewed
- [ ] Dashboard maturity score checked
- [ ] Board-ready Charter PDF generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Next lab

**Lab 05 — NCA ECC 4‑2 Cloud Security**, built around a real-world cloud misconfiguration breach.
