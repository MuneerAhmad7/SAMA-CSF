# LinkedIn Post Draft — Lab 06

---

**Main version**

In 2016, Marriott acquired Starwood Hotels. In 2018, Marriott disclosed that Starwood's reservation database had been compromised since roughly 2014 — meaning attackers had access spanning the entire acquisition, undetected for about four years. 500 million guest records exposed.

The uncomfortable question isn't "how did they get in." It's: after the acquisition closed, did Starwood's systems actually get brought under Marriott's security policy framework — or did they keep running under old assumptions while everyone assumed integration was "in progress"?

For Lab 06 of my Saudi Cybersecurity Compliance Labs series, I built the tool that answers that question with a number, not a guess.

**Policy Framework Manager** (Flask + SQLite, Dockerized, same clean UI as the last three labs):

→ A real **Policy Hierarchy** — Master Policy → Domain Policies → Standards/Procedures — rendered as an actual tree, not implied by a folder structure
→ A **Coverage Gap Analysis** that checks every required control domain against the policy register and tells you flatly: covered, or not
→ An **M&A / Third-Entity Integration Register** — exactly what should have existed for Starwood — tracking a live integration percentage and named gaps for every acquired or partner entity
→ Full policy lifecycle tracking (Draft → Review → Approved → Published → Retired) with automatic overdue-review alerts
→ A one-click, board-ready printable Policy Framework document

I seeded it with a realistic Falak Pay policy set and deliberately included the Marriott/Starwood pattern: a recent acquisition sitting at **42% policy integration**, with named gaps (Data Classification, Cryptography, and Incident Response policies not yet extended to its legacy systems). The dashboard flags it instantly as at-risk. Coverage analysis also caught a domain with literally zero policy — Cloud Security — sitting fully exposed.

That's the entire value of this exercise: Starwood's gap wasn't a mystery after the fact. It's the kind of gap that's completely visible *in advance*, if you're actually tracking coverage instead of assuming it.

Full code, case study, blank policy framework template, and a completed assessment report are on GitHub — link in comments.

Next: Lab 07 — Cloud Security, built around a real-world cloud misconfiguration breach.

#CyberSecurity #GRC #PolicyManagement #MergersAndAcquisitions #SAMA #NCA #InfoSec #SaudiArabia #RiskManagement

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Coverage Gaps page — the red "GAP — NO ACTIVE POLICY" cards next to green "COVERED" cards make the point instantly.
- A second image of the M&A Entity card showing the 42% integration bar (red) works well as a second slide.
- GitHub link goes in the first comment, not the post body.
