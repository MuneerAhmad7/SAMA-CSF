# LinkedIn Post Draft — Lab 11

---

**Main version**

The 2020 SolarWinds breach is usually told as a supply-chain attack story: malicious code slipped into a software update, distributed to 18,000 customers, undetected for months. That part's true. But the detail that stuck with me while building this lab is the part that came out afterward — public reporting and congressional testimony pointed to security weaknesses on SolarWinds' build infrastructure that had reportedly been flagged before the breach, not after.

Detection wasn't the failure. Follow-through was.

For Lab 11 of my Saudi Cybersecurity Compliance Labs series — and the piece that completes SAMA CSF Domain 1 coverage across this series — I built the tracker for exactly that gap.

**Cyber Security Audit & Assurance Tracker** (Flask + SQLite, Dockerized, same clean UI as the rest of the series):

→ An **Audit Engagement Register** covering internal audits, external audits, penetration tests, and regulatory examinations
→ A **Findings Register with severity-based remediation SLAs** — Critical: 30 days, High: 60, Medium: 90, Low: 180 — auto-computed and flagged red when overdue, the same discipline this series already applies to vulnerabilities in Lab 03
→ **Repeat-finding tracking** — because the same weakness surfacing across multiple audit cycles is itself a governance signal, separate from tracking each instance individually
→ A **Committee Reporting Log**, because a finding that never reaches a board agenda might as well not exist for governance purposes

I seeded it with a direct replay of the SolarWinds pattern: a Critical finding on build/release infrastructure access controls, first identified 690 days ago, still open, and now confirmed as a **repeat finding** in the most recent audit cycle — flagged automatically, sorted to the top of the dashboard by days overdue.

Remediation SLA compliance across the seeded dataset: 78.6%. Not bad — but the 21.4% that isn't compliant includes exactly the kind of finding that, left alone long enough, becomes the next SolarWinds.

Full code, case study, blank audit & review policy template, and a completed assessment report are on GitHub — link in comments.

#CyberSecurity #GRC #InternalAudit #SAMA #NCA #InfoSec #SaudiArabia #RiskManagement #Governance

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Dashboard's overdue findings table with the 660-day figure visible next to the repeat-finding alert banner — the number does the work.
- A second image of the Findings Register row showing "Repeat" tag with the cross-reference note works well as supporting proof.
- GitHub link goes in the first comment, not the post body.
