# Lab 07 — Cloud Security Posture Management (CSPM)
**Maps to:** SAMA CSF 4.3 (Cloud Computing) | NCA ECC 4‑2 (Cloud Computing & Hosting Cybersecurity) | NCA Cloud Cybersecurity Controls (CCC)

> Series: *Saudi Cybersecurity Compliance Labs*
> Lab 7 of N — built around the 2019 Capital One breach, the defining case study for cloud misconfiguration risk.

---

## 1. The real-world problem

**Case: Capital One, disclosed July 2019.**

A former employee of a cloud computing company exploited a **misconfigured Web Application Firewall (WAF)** protecting a Capital One web application hosted on AWS. The misconfiguration allowed a **Server-Side Request Forgery (SSRF)** attack — tricking the WAF into making requests on the attacker's behalf to AWS's internal instance metadata service. That service returned **temporary security credentials for an IAM role** attached to the WAF instance.

The critical failure: that IAM role had **far more permission than the WAF needed** — including the ability to list and read a large number of S3 storage buckets across the organization. Using the stolen credentials, the attacker enumerated and exfiltrated data from over 700 S3 buckets, exposing personal information for approximately **106 million individuals** — including names, addresses, credit scores, and in some cases Social Security numbers.

### Root causes (publicly documented, and exactly what a CSPM program exists to catch)
| Root cause | What was missing |
|---|---|
| WAF misconfigured, vulnerable to SSRF | Regular configuration review of internet-facing security controls |
| IAM role attached to the WAF had excessive permissions (far beyond least privilege) | Least-privilege IAM policy review — a role should only be able to do what its function requires |
| No effective detection of unusual, large-scale S3 access patterns | Continuous monitoring / anomaly detection on cloud data access |
| The misconfiguration existed for an extended period before discovery | Continuous Cloud Security Posture Management (CSPM) — ongoing automated scanning, not a one-time review |

This is exactly why **SAMA CSF 4.3 and NCA ECC 4‑2 require documented cloud security architecture review, least-privilege IAM, and continuous cloud security posture monitoring** — not a checklist completed once when a cloud migration begins.

## 2. What this lab builds

A **Cloud Security Posture Manager** — Flask + SQLite, same clean custom UI as Labs 03–06 — for **Falak Pay Financial Company**, that:

1. Maintains a **Cloud Resource Inventory** (S3 buckets, IAM roles, security groups, WAF ACLs, RDS/EC2 instances) with environment and sensitivity tags.
2. Runs a **Misconfiguration Findings Register** against 10 CSPM rules modeled on real cloud security failure patterns — including a direct replay of the exact Capital One pattern: an over-permissioned IAM role attached to a public-facing resource.
3. Tracks findings through a **remediation workflow** (Open → Investigating → Remediated → Verified) with severity and ownership.
4. Produces a **Dashboard** with an overall Cloud Security Posture Score, findings by severity, and critical findings requiring immediate attention.
5. Generates a **printable, audit-ready CSPM report** (`/report`).

## 3. Control mapping

| Control | Requirement | Where it's implemented |
|---|---|---|
| SAMA CSF 4.3 / ECC 4‑2‑5 | Cloud security architecture review | Cloud Resource Inventory + Findings Register |
| SAMA CSF 4.3 / ECC 4‑2‑1 | Cloud IAM, least privilege | CSPM-04, CSPM-05 (over-permissioned IAM role findings) |
| SAMA CSF 3.3 / ECC 2‑10 | Data protection (encryption, access control) | CSPM-01, CSPM-02, CSPM-03 (S3 bucket findings) |
| NCA CCC 2‑4 | Cloud monitoring and logging | CSPM-03, CSPM-10 (logging and continuous monitoring findings) |
| SAMA CSF 4.3 / ECC 4‑2‑6 | Cloud security posture management (CSPM) | This entire lab |

## 4. Environment (free/local — Docker)

```bash
cd src
docker compose up --build
# App available at http://localhost:5006
```

## 5. Step-by-step workflow

### Step 0 — Load realistic demo data
```bash
docker compose exec cspm python seed_demo_data.py
```
Seeds 12 cloud resources and 14 findings across 10 CSPM rules, including a direct replay of the Capital One pattern: an IAM role attached to a public-facing WAF/application with excessive S3 permissions.

### Step 1 — Read the case study
Open `docs/case-study-capital-one-breach.md` first.

### Step 2 — Review the Cloud Resource Inventory
Go to **Resources** — note environment (Production/Staging/Development) and sensitivity tags.

### Step 3 — Review the Findings Register
Go to **Findings** — find the Capital One-replay finding (over-permissioned IAM role on a public-facing resource) and note its severity.

### Step 4 — Work a finding through remediation
Pick a Critical/High finding, move it Open → Investigating → Remediated → Verified, with owner and notes at each step.

### Step 5 — Check the Dashboard
Review your overall Cloud Security Posture Score and severity breakdown.

### Step 6 — Generate the audit-ready report
Go to **`/report`** — print/save as PDF.

### Step 7 — Write the documentation report
Open `report/cspm-assessment-report-FILLED.md` — a completed example, ready to adapt.

## 6. What to commit to GitHub

```
lab-07-cloud-security/
├── README.md
├── docs/                 ← case study + blank CSPM policy template
├── src/                  ← Cloud Security Posture Manager app (Flask + SQLite + Docker) + seed script
├── report/               ← completed assessment report
└── screenshots/          ← dashboard + findings screenshots
```

## 7. What "done" looks like

- [ ] Demo data seeded
- [ ] Case study read
- [ ] Cloud Resource Inventory reviewed
- [ ] Capital One-replay finding identified in the Findings Register
- [ ] One finding walked through full remediation workflow
- [ ] Dashboard reviewed — posture score checked
- [ ] Audit-ready CSPM report generated
- [ ] Documentation report reviewed
- [ ] Pushed to GitHub, LinkedIn post published

## 8. Next lab

**Lab 08 — NCA ECC 3‑1 Incident Response & Forensics**, built around a real-world incident response failure.
