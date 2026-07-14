# LinkedIn Post Draft — Lab 04

---

**Main version**

In 2013, Target's security monitoring team saw alerts about the malware that would go on to expose 40 million card numbers and 70 million customer records. The alerts existed. What didn't exist was a single, empowered executive with the documented authority to act on them fast enough — Target didn't have a dedicated CISO role with direct executive access at the time. They built one after the breach.

For Lab 04 of my Saudi Cybersecurity Compliance Labs series, I stopped treating "CISO Charter" as a document you write once and file away, and built it as something you can actually assess and prove.

**CISO Charter Builder & Authority Assessment** (Flask + SQLite, Dockerized) gives you:

→ A structured Charter builder — mandate, independence from IT, budget authority, direct escalation rights, governance structure — instead of a Word doc nobody updates
→ A 14-control **Authority & Independence Assessment**, each control mapped to a specific structural gap from the Target case (Is the CISO organizationally separate from IT? Can they escalate to the Board without IT sign-off? Is there a succession plan if the CISO is unavailable during an incident?)
→ A live governance RACI matrix and Escalation Matrix — not static tables, actual tracked data
→ A one-click, board-ready printable Charter document

I ran a full self-assessment against seeded data for a fictional bank. Result: **100% Charter completeness, 82% authority maturity** — with the single biggest gap being no documented CISO succession plan. That's a real, common gap, and exactly the kind of thing this framework is built to surface before an incident, not during one.

Because here's the uncomfortable truth: a lot of organizations have a CISO *title*. Fewer have a CISO *Charter* — a document that says, in writing, exactly what that person can do, who they answer to, and how fast they can act when it matters.

Full code, case study, filled Charter template, and a completed assessment report are on GitHub — link in comments.

Next: Lab 05 — Cloud Security, built around a real-world cloud misconfiguration breach.

#CyberSecurity #GRC #CISO #Governance #SAMA #NCA #InfoSec #SaudiArabia #RiskManagement

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Dashboard showing the two progress bars (Charter completeness + Authority maturity) side by side.
- A second image of the printable `/report` Charter document (the formatted, board-ready view) works well as proof of the deliverable.
- GitHub link goes in the first comment, not the post body.
