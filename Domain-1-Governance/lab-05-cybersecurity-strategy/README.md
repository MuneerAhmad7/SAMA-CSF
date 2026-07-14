# Lab 05 — Cybersecurity Strategy & Maturity Roadmap
**Maps to:** SAMA CSF 1.2 (Cyber Security Strategy) | NCA ECC 1‑1 (Cybersecurity Strategy) | ISO 27001 Clause 5 (Leadership) | NIST CSF "Identify" function

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 5 of N — built around the 2014 Sony Pictures Entertainment hack, a case that shows what happens when security stays a reactive cost center instead of a funded, multi-year strategy.

---

## 1. The real-world problem

**Case: Sony Pictures Entertainment, November 2014.**

A group calling itself "Guardians of Peace" breached Sony Pictures' network, deployed destructive wiper malware that crippled thousands of workstations and servers, and leaked unreleased films, confidential executive emails, and personal data of employees and their families. The attack was widely attributed to North Korea, linked to Sony's planned release of a film satirizing the country's leader.

The technically striking part of this case isn't the intrusion vector — it's the **history that preceded it**. Sony had suffered a **massive breach three years earlier**, the 2011 PlayStation Network breach, which exposed data for roughly **77 million accounts** and was, at the time, one of the largest breaches in history. Internal and external commentary after the 2014 attack pointed to a consistent theme: **security investment at Sony had been treated as a reactive cost center rather than a funded, board-owned, multi-year strategy** — meaning the organizational lessons from 2011 had not translated into sustained strategic investment by 2014.

### Root causes (widely discussed in public post-incident analysis, and exactly what a Cybersecurity Strategy exists to prevent)
| Root cause | What was missing |
|---|---|
| No sustained, multi-year, board-funded security strategy | A documented 3–5 year strategy tied to business risk, reviewed and re-funded annually |
| Security treated as a cost center, underinvested relative to actual risk | Budget allocation formally tied to strategic priorities, not ad-hoc requests |
| A known, high-profile geopolitical trigger (the film's release) wasn't reflected in elevated defensive posture | A living threat-landscape assessment feeding strategic priorities |
| Lessons from the 2011 breach didn't produce lasting strategic change by 2014 | KPIs/KRIs tracking security maturity improvement over time, not just point-in-time fixes |
| No clear strategic roadmap connecting current state to target maturity | A phased roadmap (Foundation → Core → Advanced → Optimization) with owners and budgets |

This is exactly why **SAMA CSF 1.2 requires a documented 3–5 year cybersecurity strategy, reviewed annually, with budget allocation and KPIs/KRIs tied to it**, and why **NCA ECC 1‑1 requires that strategy be formally approved, communicated, and periodically reviewed** — not written once and left in a drawer.

## 2. What this lab builds

A **Cybersecurity Strategy Builder & Maturity Roadmap** tool — Flask + SQLite, same clean custom UI as Labs 03–04 — for **Falak Pay Financial Company**, that:

1. Builds a structured **Strategy document**: vision, business alignment, strategic period, threat landscape summary, budget, review cadence.
2. Runs a **Maturity Assessment** across 10 security domains, scoring **current vs. target maturity level (0–5, per the SAMA CSF maturity model)** — visualized side by side so gaps are immediately obvious.
3. Maintains a **Threat Landscape Register** — the living assessment Sony's strategy lacked — scoring threats by likelihood × impact, including geopolitical/nation-state threat categories.
4. Tracks a **Strategic Roadmap** of initiatives across four phases (Foundation, Core Controls, Advanced Controls, Optimization), each with an owner, budget, and status.
5. Produces a **Dashboard** with maturity-gap visualization, budget utilization, and initiative completion.
6. Generates a **printable, board-ready Strategy document** (`/report`).

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 1.2 / ECC 1‑1‑1 | Strategy aligned with business objectives | Strategy Builder — Business Alignment field |
| SAMA CSF 1.2 | 3–5 year horizon, annual review | Strategy Builder — Strategic Period + Review Cycle |
| SAMA CSF 1.2 | Budget allocation for cybersecurity initiatives | Strategic Roadmap — budget fields per initiative |
| SAMA CSF 1.2 | KPIs/KRIs defined and monitored | Dashboard — initiative completion, budget utilization |
| SAMA CSF 1.2 | Threat landscape analysis incorporated | Threat Landscape Register |
| SAMA CSF Maturity Model | Level 0 (Non-existent) → 5 (Adaptive), minimum Level 3 required | Maturity Assessment — current vs. target per domain |
| NCA ECC 1‑1‑2/1‑1‑3 | Strategy approved by organization head, communicated | Strategy Builder — Approved By field |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5004
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec strategy-tracker python seed_demo_data.py
```
Seeds a complete Strategy document, maturity scores for 10 domains (with realistic current/target gaps), 6 threat landscape items (including a nation-state/geopolitical entry mirroring Sony's blind spot), and 14 roadmap initiatives across all four phases.

### Step 1 — Read the case study
Open `docs/case-study-sony-pictures-hack.md` first.

### Step 2 — Review/build the Strategy document
Go to **Strategy Builder** — review vision, business alignment, threat landscape summary, budget, and review cadence.

### Step 3 — Review the Maturity Assessment
Go to **Maturity Assessment** — 10 domains, each showing current level vs. target level as a visual gap. Identify which domains have the widest current-to-target gap — these are your strategic priorities.

### Step 4 — Review the Threat Landscape Register
Go to **Threat Landscape** — note the nation-state/geopolitical entry. Ask yourself: does your organization's strategy actually reflect elevated risk during high-profile or controversial periods, the way Sony's should have in 2014?

### Step 5 — Review the Strategic Roadmap
Go to **Roadmap** — 14 initiatives phased Foundation → Optimization. Update one initiative's status and budget spent, and watch the Dashboard's completion metrics update.

### Step 6 — Check the Dashboard
Review overall maturity gap, budget utilization, and initiative completion by phase.

### Step 7 — Generate the board-ready Strategy document
Go to **`/report`** — print/save as PDF.

### Step 8 — Write the documentation report
Open `report/cybersecurity-strategy-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-05-cybersecurity-strategy/
├── README.md
├── docs/                 ← case study + blank strategy template
├── src/                  ← Strategy Builder app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + printable strategy screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Strategy document reviewed
- [ ] Maturity Assessment reviewed — widest gaps identified
- [ ] Threat Landscape Register reviewed, including geopolitical entry
- [ ] One roadmap initiative updated end to end
- [ ] Dashboard reviewed
- [ ] Board-ready Strategy PDF generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Next lab

**Lab 06 — NCA ECC 4‑2 Cloud Security**, built around a real-world cloud misconfiguration breach.
