# LinkedIn Post Draft — Lab 01

---

**Option A — Build-in-public style**

🇸🇦 Day 1 of my "90 Days of Saudi Cybersecurity Compliance Labs" series: Governance.

Most people think SAMA CSF / NCA ECC compliance starts with firewalls and SIEMs. It actually starts with something less exciting but far more failed-on-audit: governance evidence.

So I built a self-hosted Governance & Compliance Tracker (Flask + SQLite, Dockerized) that models what a real GRC analyst runs day-to-day:
→ Policy lifecycle tracking (Draft → Approved → Published)
→ RACI matrix for cybersecurity accountability
→ Cyber Security Committee meeting log with action items
→ KPI/KRI dashboard with RAG status
→ Live compliance scoring against all 19 SAMA CSF 1.1–1.9 + NCA ECC 1‑1→1‑10 controls

Plus the actual documents an auditor asks for: governance charter, Board-approved policy, RACI matrix, quarterly Board report — and a full governance assessment report template.

Everything's on GitHub (code + docs + workflow) — link in comments.

Next: Lab 02 — Identity & Access Management (NCA ECC 2‑2), hands-on with local MFA/PAM.

#CyberSecurity #GRC #SAMA #NCA #InfoSec #SaudiArabia #ComplianceAsCode

---

**Option B — Lesson-led style**

Here's a governance mistake I keep seeing in KSA compliance programs: policies exist, but nobody can *prove* the Board approved them, reviewed them, or that staff acknowledged them.

SAMA CSF 1.3 and NCA ECC 1‑3 don't just ask "do you have a policy" — they ask for evidence of the full lifecycle.

I built a small open-source tracker to solve exactly this — [1-line description]. Full lab, code, and templates on GitHub.

#CyberSecurity #GRC #ComplianceEngineering

---

*Tip: attach 1–2 dashboard screenshots and the architecture diagram when posting — governance posts perform better with a visual than a wall of text.*
