# Case Study: The Target Corporation Breach (2013)

*This account is compiled from widely reported public facts about the incident, summarized in the author's own words for educational use in this lab.*

## Timeline
1. Attackers obtained network credentials from a third-party HVAC/refrigeration vendor with remote access into Target's network for billing and project management purposes.
2. Using that foothold, attackers moved laterally into Target's point-of-sale (POS) systems and installed malware designed to capture payment card data as cards were swiped in stores.
3. Target's security team had commercial threat-detection tooling in place (monitored partly through a third-party security operations center) that **generated alerts about the malicious activity before the breach became public**.
4. Despite these alerts, the response was not decisive or fast enough to stop the exfiltration of data before the intrusion became a large-scale breach.
5. The breach, disclosed in December 2013, ultimately affected payment card data for roughly **40 million accounts** and personal information for approximately **70 million customers**.
6. In the aftermath, Target's public remediation commitments included structural governance changes — notably, creating a **dedicated Chief Information Security Officer position with a direct reporting line to executive leadership**, something the organization had not had in place at the time of the breach.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | Alerts generated but not decisively actioned | A single accountable executive with clear, documented authority to mobilize an incident response | Charter Builder — Mandate & Authority section |
| 2 | No dedicated CISO role with executive/board access | CISO independent from IT, with a defined reporting line | Authority Assessment controls #1–#3 |
| 3 | Unclear ownership of "who can act" during a security event | Documented, board-approved escalation authority | Escalation Matrix module |
| 4 | Structure built reactively, after the breach | A Charter defining role, authority, and independence *proactively* | This entire lab |

## Why this matters under SAMA/NCA
- **SAMA CSF 1.1** requires a dedicated cybersecurity function independent from IT, with a CISO reporting to the Board or CEO — precisely the structural gap identified in Target's post-breach remediation.
- **NCA ECC 1‑2‑6** requires organizational separation between the cybersecurity function and IT operations, to avoid the "buried in IT" problem where security decisions compete with operational priorities and lose.
- **NCA ECC 1‑2‑2** requires the cybersecurity leader to be appointed "with appropriate authority and qualifications" — authority being the operative word, not just a title.
- **SAMA CSF 5.1** (Incident Management Framework) requires documented escalation procedures — the mechanism that turns "we saw an alert" into "we acted."

## Discussion questions for your LinkedIn/portfolio writeup
- What's the difference between a CISO who has a title and a CISO who has a *Charter* with real authority?
- If your organization's monitoring team saw a critical alert at 2 AM, is it documented, right now, exactly who has the authority to act — and how fast?
- Where in your own organization does security currently report, and does that reporting line create the same kind of structural gap Target had in 2013?
