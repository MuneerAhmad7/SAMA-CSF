# LinkedIn Post Draft — Lab 02

---

**Main version**

In February 2016, attackers used stolen SWIFT credentials to try to steal $951 million from Bangladesh Bank. $81 million actually got out — laundered through casinos in the Philippines before it could be stopped.

The fraud was only discovered because a printer ran out of paper.

No MFA on the payment terminal. No segregation of duties between who could create a transfer and who could release it. No real-time fraud detection. No centralized alerting.

Every one of those gaps is now a named control under SAMA CSF and NCA ECC. So for Lab 02 of my Saudi Cybersecurity Compliance Labs series, I didn't build a generic IAM demo — I rebuilt the exact failure chain from this incident, then closed it.

**SecurePay** (Flask + SQLite, Dockerized) implements:
→ Mandatory TOTP-based MFA at login — no exceptions, no bypass
→ Maker-checker segregation of duties, enforced server-side — a Maker cannot approve their own payment, and the attempt is logged as a security event
→ A real-time fraud detection engine that flags the exact heist pattern: high-value transfers to first-time beneficiaries, off-hours submissions, transaction velocity spikes, high-risk destination countries
→ A full audit trail and security dashboard — the thing that would have caught this in minutes instead of days

I ran the attack pattern against my own system: created a 20M SAR transfer to a new beneficiary at 2 AM. The fraud engine flagged it as HIGH risk on the spot, before a human even looked at it.

Full code, control mapping, policy templates (Segregation of Duties policy, Payment Authorization Matrix), and an incident postmortem template are on GitHub — link in comments.

Next: Lab 03 — Vulnerability Management, modeled on the 2017 Equifax breach.

#CyberSecurity #GRC #Banking #FraudPrevention #SAMA #NCA #InfoSec #SaudiArabia #FinTech #RiskManagement

---
NOTES FOR POSTING (delete before publishing):
- Screenshot the dashboard showing the HIGH-risk flagged transaction — this is your strongest visual.
- A short screen-recording GIF of the self-approval attempt being blocked performs very well on LinkedIn for GRC/security audiences.
- Put the GitHub link in the first comment, not the post body.
