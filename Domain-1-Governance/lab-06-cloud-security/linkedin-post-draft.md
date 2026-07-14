# LinkedIn Post Draft — Lab 07

---

**Main version**

In 2019, an attacker exploited a misconfigured Web Application Firewall to trick it into requesting AWS credentials from an internal metadata service. Those credentials belonged to an IAM role attached to the WAF — a role with far more permission than a WAF should ever need, including the ability to list and read 700+ S3 buckets.

106 million people's data exposed. Not because of some exotic zero-day. Because a role had "just in case" permissions that nobody scoped back down.

For Lab 07 of my Saudi Cybersecurity Compliance Labs series, I built the tool that would have caught this before it became a headline.

**Cloud Security Posture Manager** (Flask + SQLite, Dockerized, same clean UI as the last four labs):

→ A **Cloud Resource Inventory** — every S3 bucket, IAM role, security group, and WAF ACL tracked with environment and sensitivity tags
→ A **10-rule Findings Register** modeled on real cloud misconfiguration patterns — public buckets, wildcard IAM permissions, exposed database ports, missing encryption, and the exact Capital One pattern: an over-permissioned role on a public-facing resource
→ A weighted **Cloud Security Posture Score** — not a vanity number, a real 100-point score that drops hard for unresolved Critical findings
→ A full remediation workflow (Open → Investigating → Remediated → Verified) with ownership and audit logging
→ A one-click, audit-ready printable report

I seeded it with a realistic dataset and deliberately replayed the Capital One pattern: an IAM role attached to a public-facing WAF with account-wide S3 read access. Posture score: **32/100**. Four open Critical findings. Not a hypothetical — exactly the kind of gap that sits quietly in a lot of real cloud environments until someone finds it first.

That's the whole point of CSPM: find it before someone else does, continuously, not once during initial deployment and never again.

Full code, case study, blank cloud security policy template, and a completed assessment report are on GitHub — link in comments.

Next: Lab 08 — Incident Response & Forensics, built around a real-world incident response failure.

#CyberSecurity #GRC #CloudSecurity #AWS #SAMA #NCA #InfoSec #SaudiArabia #CSPM #RiskManagement

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Dashboard's posture score gauge (the red/orange circle) next to the Critical findings table — the visual severity is the hook.
- A second image of the Findings page filtered to Critical, showing the Capital One-replay finding with its full description, works well as supporting proof.
- GitHub link goes in the first comment, not the post body.
