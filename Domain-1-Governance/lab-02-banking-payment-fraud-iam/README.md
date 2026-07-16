# Lab 02 — Privileged Access, Segregation of Duties & Payment Fraud Detection
**Maps to:** SAMA CSF 3.1 (IAM), 3.7 (Payment Systems Security), 1.4 (Segregation of Duties) | NCA ECC 2‑2 (IAM), 2‑5 (Event Logs & Monitoring), 1‑4 (Roles & Responsibilities)

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 2 of N — this one is built directly around a real bank heist, not a hypothetical.

---

## 1. The real-world problem

**Case: the Bangladesh Bank / SWIFT heist, February 2016.**

Attackers compromised Bangladesh Bank's SWIFT payment terminal credentials (via malware introduced through the bank's network) and used them to issue **fraudulent transfer instructions to the Federal Reserve Bank of New York**, attempting to move roughly **$951 million** out of the bank's account. Most requests were blocked by manual/automated review, but **around $81 million was successfully transferred to accounts at Rizal Commercial Banking Corporation (RCBC) in the Philippines**, then laundered through casinos before most of it could be recovered. One further transfer — intended for a Sri Lankan NGO — was stopped after a bank employee noticed the beneficiary's name was misspelled.

### Root causes (publicly documented, and the exact things regulators now mandate against)
| Root cause | What was missing |
|---|---|
| Stolen SWIFT terminal credentials used freely | No mandatory MFA on the payment terminal |
| A single compromised user could originate *and* release high-value transfers | No maker-checker / segregation of duties enforced in the payment system itself |
| 35 transfer requests fired in a short window, many to new beneficiaries, outside normal patterns | No real-time transaction anomaly/fraud detection |
| No one at the bank was alerted until correspondent banks and media noticed | No centralized security monitoring / alerting on payment system activity |
| Old, unsegmented network hardware connecting the SWIFT terminal | No network segmentation between payment systems and general IT |

This single incident is why **SAMA CSF explicitly calls out SWIFT CSP compliance (3.7)**, why **MFA for privileged/payment systems is mandatory (3.1)**, and why **segregation of duties is a named control (1.4, ECC 1‑4‑3)** rather than a "nice to have."

## 2. What this lab builds

A small, self-contained **"SecurePay" interbank payment simulator** — a Flask + SQLite app — that implements the controls that *would have stopped* the Bangladesh Bank heist:

1. **Mandatory MFA (TOTP)** for every user, enforced at login — no privileged action possible without it.
2. **Maker-checker segregation of duties** — a payment must be created by one user (Maker) and approved by a *different* user (Checker). The system actively blocks and logs any attempt at self-approval.
3. **Real-time fraud detection rule engine** that flags transactions matching the actual heist pattern:
   - High-value transfer to a **first-time beneficiary**
   - Transfer submitted **outside business hours**
   - **Velocity check**: multiple transfers to the same beneficiary in a short window
   - Beneficiary country on a **high-risk destination list**
4. **Immutable-style audit log** of every login, payment action, approval, rejection, SoD-violation attempt, and fraud flag — the thing that was missing and cost investigators weeks of reconstruction after the real incident.
5. **Security dashboard** showing flagged transactions, blocked SoD violations, and full audit trail — this is what a SOC/fraud desk screen would look like.

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 3.1 / ECC 2‑2‑5 | MFA for privileged accounts, admin consoles, customer-facing apps | TOTP enforced at login for all roles |
| SAMA CSF 3.1 / ECC 2‑2‑3 | Privileged Access Management, least privilege | Role model: Maker / Checker / Admin, enforced server-side on every route |
| SAMA CSF 1.4 / ECC 1‑4‑3 | Segregation of duties | Maker cannot approve own payment — attempt is blocked + logged |
| SAMA CSF 3.7 | Payment systems security, transaction monitoring, fraud detection | Rule engine (`fraud_engine.py`) |
| SAMA CSF 3.3 / ECC 2‑5 | Event logs and monitoring, 24/7 monitoring capability | `AuditLog` model + Security Dashboard |
| SAMA CSF 5.3 | Incident reporting (SAMA within 2h for critical) | `report/incident-postmortem-template.md` |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5001
```

Stack: Flask + SQLite + `pyotp` (TOTP MFA) + `qrcode` (for enrolling an authenticator app). No cloud account, no external services.

## 5. Step-by-step workflow

### Step 1 — Read the case study
Open `docs/case-study-bangladesh-bank-heist.md` first. Every control you build in this lab maps back to a specific line in that timeline.

### Step 2 — Enroll two users with MFA
1. Go to `/register`, create **Maker_Ahmed** (role: Maker) and **Checker_Sara** (role: Checker).
2. Each registration shows a QR code — scan it with Google Authenticator / Authy (or any TOTP app), or just copy the secret in manually.
3. Log in as each user using username + password + the 6-digit TOTP code. **Login is refused without a valid TOTP code** — this alone is the control the real SWIFT terminal lacked.

### Step 3 — Attempt the heist pattern (and watch it get caught)
As **Maker_Ahmed**:
1. Create a payment: high value (e.g., 50,000,000 SAR), a **brand-new beneficiary** you haven't used before, submit it at, say, 2 AM system time (there's a "simulate off-hours" toggle for demo purposes) → the fraud engine will auto-flag it as **HIGH RISK** the moment it's created. Note the reasons shown.
2. Try to approve your own payment as Maker_Ahmed → **blocked**, and the attempt is written to the audit log as an SoD violation. This is the exact single-point-of-failure that let $81M walk out the door in 2016.

### Step 4 — Play Checker
1. Log out, log in as **Checker_Sara**.
2. Go to the pending approvals queue — you'll see Ahmed's payment with its fraud flags clearly displayed.
3. Reject it (with a reason) — this is the human control layer that stopped 34 of the 35 real fraudulent requests.
4. Create a *second*, legitimate-looking small payment as Maker_Ahmed, to a known/repeat beneficiary, during business hours → notice it does **not** get flagged, and Sara can approve it cleanly.

### Step 5 — Review the Security Dashboard
Go to `/dashboard` (any logged-in user) and review:
- Total flagged transactions and by which rule
- Blocked SoD-violation attempts
- Full audit trail (timestamp, actor, action, target)

### Step 6 — Write the incident postmortem
Copy `report/incident-postmortem-template.md`, and write it up **as if** the flagged transaction in Step 3 had actually gone through — this is the exercise of thinking like the fraud/incident response team, using the real Bangladesh Bank timeline as your model.

## 6. What to commit to GitHub

```
lab-02-banking-payment-fraud-iam/
├── README.md
├── docs/                 ← case study + SoD policy + authorization matrix
├── src/                  ← SecurePay app (Flask + SQLite + Docker)
├── report/               ← completed incident postmortem
└── screenshots/          ← dashboard + fraud-flag screenshots
```

## 7. What "done" looks like

- [ ] Two users enrolled with working TOTP MFA
- [ ] One high-risk payment created and auto-flagged by the rule engine
- [ ] One self-approval attempt blocked and logged (SoD proof)
- [ ] One payment properly rejected by a Checker with a documented reason
- [ ] One legitimate payment created, reviewed, and approved cleanly
- [ ] Security dashboard screenshot captured
- [ ] Incident postmortem written using the real case as a model
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Why this matters for a banking employer

This lab is deliberately built around a breach that **actually happened to a central bank**, not a toy CTF scenario. Being able to say *"I rebuilt the exact control failures behind the Bangladesh Bank SWIFT heist and implemented the fixes SAMA now mandates"* is a materially stronger portfolio statement than "I read about IAM."
