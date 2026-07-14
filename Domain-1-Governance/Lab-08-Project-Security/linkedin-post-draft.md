# LinkedIn Post Draft — Lab 08

---

**Main version**

In 2018, a single malicious script ran on British Airways' payment checkout page for about two and a half weeks, quietly capturing card numbers and CVVs as customers typed them, while every transaction completed normally. 380,000 people's payment data exposed. One of the largest GDPR fines ever proposed at the time.

The technical mechanism was almost incidental. The real question is: how did a change reach the live payment page without anyone catching it — and why did nobody notice for over two weeks once it did?

For Lab 08 of my Saudi Cybersecurity Compliance Labs series, I built the control that answers that question before it becomes a breach.

**Project Security Gate Tracker** (Flask + SQLite, Dockerized, same clean UI as the last five labs):

→ A **6-gate Security Pipeline** — Initiation → Design → Build → Test → Deploy → Post-Implementation — for every project, with a named approver required at each gate
→ A **Third-Party Script / Code Integrity Register** tracking every script on customer-facing pages and whether it has Subresource Integrity (SRI) protection — exactly the control missing at BA
→ A **Change Log** that flags any production deployment that went live without its Deploy gate actually Passed
→ A one-click, audit-ready printable report

I seeded it with 6 realistic projects and deliberately replayed the BA pattern: a Critical payment project with its Deploy gate marked "Waived" under deadline pressure, followed by an ungated hotfix deployed straight to the live payment page — sitting right next to a third-party analytics script on that same page with no SRI hash pinned and unreviewed for 7 months.

That's not a hypothetical. That's the exact structural shape of the British Airways breach, reproduced in miniature, and caught by the dashboard the moment it happens instead of two and a half weeks later.

The lesson underneath this lab: a documented security gate process only works if it can't be quietly waived under pressure. Documentation isn't the control. Enforcement is.

Full code, case study, blank project security policy template, and a completed assessment report are on GitHub — link in comments.

Next: Lab 09 — Incident Response & Forensics, built around a real-world incident response failure.

#CyberSecurity #GRC #SDLC #ApplicationSecurity #SAMA #NCA #InfoSec #SaudiArabia #SecureCoding #RiskManagement

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the gate pipeline on the Payment Checkout Redesign project — the visual row of gates with one showing "Waived" in amber tells the story instantly.
- A second image of the Change Log row flagged "✗ NO — UNGATED CHANGE" in red works well as supporting proof.
- GitHub link goes in the first comment, not the post body.
