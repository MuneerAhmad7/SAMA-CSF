# Lab 10 — AI Governance & Model Risk Evidence
**Extends:** SAMA CSF 1.2 (Strategy), 2.2 (Risk Assessment), 1.5 (Project Security) | NCA ECC 1‑5 (Risk Management) | Referenced against NIST AI RMF, ISO/IEC 42001 — since neither SAMA CSF nor NCA ECC yet define a dedicated AI control domain.

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 10 of N — the odd one out in this series, and deliberately so.

---

## 0. Why this lab is different

Every other lab in this series maps to an explicit SAMA CSF or NCA ECC control number, because the control being evidenced is **deterministic**: a policy either exists or it doesn't (Lab 01), a patch is either applied within SLA or it isn't (Lab 03), a Deploy gate is either Passed or Waived (Lab 08). You can point an auditor at a single record and say "here is the evidence."

AI systems break that model. A generative chatbot, a fraud-scoring model, an internal copilot — **the same input can produce a different output on every run.** SAMA CSF and NCA ECC, written before this was a mainstream operational reality, implicitly assume you can point to a fixed, testable control. Neither framework yet says, in so many words, "here is how a Board evidences oversight of a system whose behavior is probabilistic, not deterministic." Nobody's shipped a tracker for that gap — so this lab builds one, deliberately framed as *emerging practice extending existing GRC principles*, not as a claim that SAMA/NCA have published AI-specific controls they haven't.

## 1. The real-world problem

**Case: Air Canada's chatbot, 2022–2024.**

A customer used Air Canada's website chatbot to ask about bereavement fares after a family death. The chatbot told him he could book a full-price ticket and apply for a bereavement discount retroactively within 90 days — advice that **did not match Air Canada's actual policy**, which required the discount request before travel. When the customer later tried to claim the refund the chatbot had promised, Air Canada refused, arguing in the subsequent tribunal case that **the chatbot was "a separate legal entity" responsible for its own words** — a defense the British Columbia Civil Resolution Tribunal rejected outright in February 2024, ruling Air Canada liable and ordering it to pay damages.

### Root causes (publicly documented, and exactly the gap this lab's controls target)
| Root cause | What was missing |
|---|---|
| No human-in-the-loop checkpoint for policy-sensitive answers (refunds, exceptions) | A defined, enforced escalation trigger: certain topics must route to a human, regardless of model confidence |
| No apparent sampling/review process checking chatbot answers against actual policy | Periodic statistical review of AI outputs — since you cannot review every possible output, you review a representative sample and track accuracy over time |
| No clear organizational accountability for what the AI said | An explicit model-owner and incident process treating a wrong AI answer exactly like any other customer-facing error |
| The company's own legal defense revealed no governance narrative existed | A change-control and oversight record a company can actually point to, showing the system was managed, not just deployed and left alone |

## 2. What this lab builds

An **AI Governance & Model Risk Evidence Tracker** — Flask + SQLite, same clean custom UI as Labs 03–09 — for **Falak Pay Financial Company**, that answers the framing question directly: **you evidence oversight of a non-deterministic system with aggregate, sampled, trended evidence — not a single static checkbox.**

1. An **AI System Inventory** — every AI/ML system in use, risk-tiered by customer-facing impact and decision autonomy.
2. **Human Oversight Checkpoints** per system — explicit, named triggers where the system must hand off to a human, and whether that checkpoint is actually enforced in production (not just documented).
3. An **Output Sample Review Log** — the core mechanic. Instead of testing "the" output, reviewers periodically sample a batch of real outputs, score them against a rubric, and the tracker computes a rolling accuracy rate over time. **This sampled, trended number is the Board evidence** for a system that can't be tested exhaustively.
4. An **Incident Log** — every time an AI output caused a real problem, tracked exactly like a security incident, with root cause and remediation.
5. A **Model Change Log** — every model version upgrade, prompt change, or guardrail update, gated through an approval step before reaching production (the AI-specific equivalent of Lab 08's Deploy gate).
6. A **Dashboard** presenting the kind of aggregate, defensible summary a Board or auditor actually needs: weighted sample accuracy %, open incidents, unenforced checkpoints, pending model changes.
7. A **printable, board-ready report** (`/report`).

## 3. Control mapping (extension, not a citation)

| Principle | Traditional deterministic equivalent | AI/non-deterministic implementation in this lab |
|---|---|---|
| Governance strategy covers emerging tech (SAMA CSF 1.2) | Strategy document names the technology | AI System Inventory + risk tiering |
| Segregation of duties / human sign-off (SAMA CSF 1.4, 1.5) | Maker-checker on a transaction | Human Oversight Checkpoints, enforced per risk tier |
| Vulnerability/patch SLA (SAMA CSF 3.3) | A CVE is Open until Verified | Incident Log — an AI failure is Open until Resolved, with root cause |
| Change management / Deploy gate (SAMA CSF 1.5, NCA ECC 2‑8) | Code change requires sign-off before prod | Model Change Log — prompt/model/guardrail changes require Approved status before "live" |
| Compliance monitoring (NCA ECC 1‑3‑6) | A control is checked as implemented/not | Output Sample Review — a *rate*, sampled and trended, replaces a binary check |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5009
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec ai-governance python seed_demo_data.py
```
Seeds 5 AI systems (including the Customer Support Chatbot first introduced in Lab 08), oversight checkpoints, several output sample review batches, an incident record that directly replays the Air Canada scenario, and a model change log with one pending approval.

### Step 1 — Read the case study
Open `docs/case-study-air-canada-chatbot.md` first.

### Step 2 — Review the AI System Inventory
Go to **AI Systems** — note risk tiers and which systems are customer-facing.

### Step 3 — Review Oversight Checkpoints
Open the Customer Support Chatbot — find the refund/policy-exception checkpoint and check whether it's marked enforced.

### Step 4 — Review the Output Sample Review Log
Go to **Sample Reviews** — this is the heart of the lab. See how a rolling accuracy percentage is computed from periodic sampling instead of a one-time pass/fail.

### Step 5 — Review the Incident Log
Find the seeded incident that replays the Air Canada scenario, and read its root cause and remediation.

### Step 6 — Review the Model Change Log
Find the pending model change and approve or reject it.

### Step 7 — Check the Dashboard
Review the weighted sample accuracy %, open incidents, and unenforced checkpoints — this is what you'd actually present to a Board.

### Step 8 — Generate the board-ready report
Go to **`/report`** — print/save as PDF.

### Step 9 — Write the documentation report
Open `report/ai-governance-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-10-ai-governance/
├── README.md
├── docs/                 ← case study + blank AI governance policy template
├── src/                  ← AI Governance Evidence Tracker app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + sample review screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] AI System Inventory reviewed, risk tiers understood
- [ ] Oversight checkpoint gap identified on the chatbot
- [ ] Output Sample Review Log reviewed — understand how the rolling accuracy % is built
- [ ] Air Canada-replay incident reviewed
- [ ] Pending model change approved/rejected
- [ ] Dashboard reviewed
- [ ] Board-ready report generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. A note on intellectual honesty for this lab specifically

Unlike Labs 01–09, this lab does **not** map to explicit, numbered SAMA CSF or NCA ECC controls, because those controls don't yet exist in the source material this series is built from. Say so plainly if you present this lab: it's a demonstration of applying GRC first principles — governance, human accountability, sampled assurance, change control — to a gap the named frameworks haven't caught up to yet. That's a stronger portfolio signal than pretending a citation exists.

## 9. Next lab

**Lab 11 — NCA ECC 3‑1 Incident Response & Forensics**, built around a real-world incident response failure.
