# Lab 06 — Policy Framework, Coverage & M&A Integration
**Maps to:** SAMA CSF 1.3 (Policy), 4.2 (Outsourcing) | NCA ECC 1‑3 (Policies & Procedures), 4‑1 (Third-Party Cybersecurity) | ISO 27001 A.5.1

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 6 of N — built around the Marriott/Starwood breach, the textbook case of what happens when a policy framework doesn't follow an acquisition.

---

## 1. The real-world problem

**Case: Marriott International / Starwood Hotels, disclosed 2018.**

In November 2018, Marriott disclosed that an unauthorized party had accessed the Starwood guest reservation database, exposing personal data for approximately **500 million guests** — including passport numbers and, for some, payment card information. The intrusion into Starwood's systems is believed to have begun around **2014**, meaning attackers had access for roughly **four years**, spanning Marriott's **2016 acquisition of Starwood**, before discovery in September 2018.

The detail most relevant to this lab isn't the technical intrusion vector — it's what happened (or didn't happen) at the moment of acquisition. Marriott had its own information security program. Starwood had its own, separate systems and — by every indication from the timeline — its own, separate, **already-compromised** environment. Post-acquisition, Marriott's cybersecurity policy framework was not fully, promptly extended and harmonized across the newly acquired Starwood estate. The compromised reservation database kept running, under old assumptions, for years inside the combined company.

### Root causes (widely discussed in public post-incident analysis, and exactly what a policy framework exists to prevent)
| Root cause | What was missing |
|---|---|
| Starwood's systems weren't promptly brought under Marriott's unified policy framework | A documented M&A security integration policy with a hard timeline |
| No framework-wide gap analysis after the acquisition closed | A coverage analysis mapping every control domain against every business unit/subsidiary |
| Legacy Starwood systems continued operating under old (weaker) standards | Policy inheritance/harmonization tracking — knowing exactly which systems are and aren't covered |
| The compromise went undetected for ~4 years, spanning the acquisition | Consistent monitoring/logging policy applied uniformly across all acquired entities, not just the "core" business |

This is exactly why **SAMA CSF 4.2 requires SAMA approval and documented due diligence for critical outsourcing/acquisitions**, why **NCA ECC 4‑1 requires ongoing third-party monitoring**, and why a mature **Policy Framework** must explicitly track *scope of coverage* — not just "we have a policy," but "we have a policy, and here is proof it actually applies to every system and entity it needs to."

## 2. What this lab builds

A **Policy Framework Manager** — Flask + SQLite, same clean custom UI as Labs 03–05 — for **Falak Pay Financial Company**, that:

1. Maintains a full **Policy Register** with lifecycle tracking (Draft → Review → Approved → Published → Retired), version control, and review-SLA overdue alerts.
2. Renders the **Policy Hierarchy** as a real tree — Master Policy → Domain Policies → Standards/Procedures — so the structure is visible, not implied.
3. Runs a **Coverage Gap Analysis** — checks every required control domain (Governance, IAM, Data Protection, Cryptography, Incident Response, BCP, Third-Party, HR, Physical, Cloud, Awareness) against the policy register and flags any domain with no current Approved/Published policy.
4. Tracks an **M&A / Third-Entity Integration Register** — exactly the tool that should have existed for the Starwood integration — listing every acquired or partner entity with a live policy-framework integration percentage and named gaps.
5. Produces a **Dashboard** showing framework completeness, coverage gaps, overdue reviews, and integration risk.
6. Generates a **printable, board-ready Policy Framework document** (`/report`).

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 1.3 / ECC 1‑3‑1 | Comprehensive, Board-approved policy | Policy Register — Master Policy record |
| SAMA CSF 1.3 / ECC 1‑3‑2 | Supporting policies for each subdomain | Policy Hierarchy — Domain Policies |
| SAMA CSF 1.3 / ECC 1‑3‑4 | Annual review cycle | Policy Register — review_date SLA tracking |
| SAMA CSF 4.2 / ECC 4‑1‑2 | Vendor/acquisition due diligence, ongoing monitoring | M&A / Third-Entity Integration Register |
| NCA ECC 1‑3‑6 | Compliance monitoring | Coverage Gap Analysis |
| SAMA CSF 4.2 | Data residency, right-to-audit for outsourcing | Entity register — scope/risk notes |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5005
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec policy-framework python seed_demo_data.py
```
Seeds a full Falak Pay policy set (1 Master Policy, domain policies across 11 control domains, supporting standards/procedures), 3 tracked entities (a wholly-owned subsidiary, a recent acquisition, and a third-party partner) with realistic integration gaps, and one deliberately overdue policy review.

### Step 1 — Read the case study
Open `docs/case-study-marriott-starwood-breach.md` first.

### Step 2 — Review the Policy Hierarchy
Go to **Hierarchy** — see the full tree from Master Policy down to individual Standards/Procedures.

### Step 3 — Run the Coverage Gap Analysis
Go to **Coverage Gaps** — check which control domains have no current Approved/Published policy.

### Step 4 — Review the M&A / Third-Entity Integration Register
Go to **Entities** — note the seeded acquisition sitting at a low integration percentage, with explicit gap notes. This is the exact register that should have existed for Starwood.

### Step 5 — Work a policy through its lifecycle
Pick a Draft policy, move it to Review, then Approved, then Published — watch the audit log and dashboard update.

### Step 6 — Check the Dashboard
Review framework completeness, overdue reviews, and integration risk.

### Step 7 — Generate the board-ready document
Go to **`/report`** — print/save as PDF.

### Step 8 — Write the documentation report
Open `report/policy-framework-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-06-policy-framework/
├── README.md
├── docs/                 ← case study + blank policy framework template
├── src/                  ← Policy Framework Manager app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + hierarchy + printable report screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Policy Hierarchy reviewed end to end
- [ ] Coverage Gap Analysis run — any gaps identified and noted
- [ ] M&A/Entity Integration Register reviewed
- [ ] One policy walked through its full lifecycle
- [ ] Dashboard reviewed
- [ ] Board-ready Policy Framework PDF generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Next lab

**Lab 07 — NCA ECC 4‑2 Cloud Security**, built around a real-world cloud misconfiguration breach.
