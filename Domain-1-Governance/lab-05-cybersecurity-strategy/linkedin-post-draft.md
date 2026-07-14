# LinkedIn Post Draft — Lab 05

---

**Main version**

In 2011, Sony suffered one of the largest breaches in history at the time — 77 million PlayStation Network accounts exposed. Three years later, Sony Pictures got hit again: destructive wiper malware, leaked films, leaked executive emails, employee data exposed. Same parent company. Three years apart.

The uncomfortable question post-incident analysis kept circling back to: what actually changed strategically between 2011 and 2014? By most public accounts — not enough. Security had reportedly stayed a reactive cost center rather than becoming a sustained, funded, board-owned strategic priority.

For Lab 05 of my Saudi Cybersecurity Compliance Labs series, I built the tool that's supposed to prevent exactly that pattern: a strategy that exists on paper once, versus one that's actually tracked, funded, and revisited.

**Cybersecurity Strategy Builder & Maturity Roadmap** (Flask + SQLite, Dockerized, same clean UI as the last two labs):

→ A structured Strategy document — vision, business alignment, threat landscape, multi-year budget, governance cadence
→ A **Maturity Assessment** across 10 domains, visualizing current level vs. target level side by side, so the gaps are impossible to miss
→ A **Threat Landscape Register** scored by likelihood × impact — including a standing Nation-State/Geopolitical category, because a foreseeable geopolitical trigger going unreflected in defensive posture was exactly Sony Pictures' blind spot
→ A **phased Roadmap** (Foundation → Core → Advanced → Optimization) with real budget tracking, not just a slide that says "improve security"
→ A one-click, board-ready printable Strategy document

Running it against seeded data for a fictional bank: 100% strategy completeness, but average maturity sitting at 2.3 against a 3.7 target — an honest, visible gap instead of a strategy doc that quietly goes stale in a shared drive.

That gap being visible is the entire point. A strategy nobody can measure against isn't a strategy — it's a memo.

Full code, case study, blank strategy template, and a completed assessment report are on GitHub — link in comments.

Next: Lab 06 — Cloud Security, built around a real-world cloud misconfiguration breach.

#CyberSecurity #GRC #Strategy #SAMA #NCA #InfoSec #SaudiArabia #RiskManagement #CISO

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Maturity Assessment page — the current-vs-target bar visualization with the red target markers is the strongest single image in this lab.
- A second image of the Roadmap phase progress bars (Foundation 100%, Core Controls 0%, etc.) tells the "we're 18 months in" story visually.
- GitHub link goes in the first comment, not the post body.
