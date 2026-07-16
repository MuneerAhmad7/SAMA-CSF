# Case Study: The SolarWinds Breach (Disclosed December 2020)

*This account is compiled from widely reported public facts about the incident, including subsequent public congressional testimony and reporting, summarized in the author's own words for educational use in this lab.*

## Timeline
1. At some point before 2020, attackers gained access to SolarWinds' software development/build environment for its Orion IT management platform.
2. Attackers inserted malicious code — later named "Sunburst" — into legitimate Orion software updates.
3. These trojanized updates were digitally signed and distributed through SolarWinds' normal update mechanism to approximately **18,000 customers**, including multiple U.S. federal agencies and numerous large private-sector organizations.
4. The compromise was discovered and disclosed in **December 2020** by a cybersecurity firm that identified the malicious activity during its own incident response process — not by SolarWinds' internal detection.
5. In the aftermath, public reporting and congressional testimony surfaced additional context: **security weaknesses in SolarWinds' infrastructure had reportedly been identified before the breach**, including a since widely-reported incident where a security researcher had flagged an update server accessible with a weak, easily-guessed password. Some public reporting also referenced earlier internal assessments having raised concerns about security practices.
6. The core governance question that emerged from post-incident scrutiny wasn't "was a vulnerability found" — reviews and external warnings evidently existed — but **"what happened after it was found, and was it tracked to actual remediation."**

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | Known weaknesses on build/release infrastructure not remediated before the breach | A tracked findings register with severity-based remediation SLAs | Findings Register — auto-computed due dates, overdue flagged |
| 2 | No visible escalation as findings aged | Overdue-finding alerting to leadership | Dashboard — overdue findings surfaced prominently |
| 3 | Findings on the build pipeline weren't treated with urgency proportional to their potential blast radius | Severity/business-impact-based prioritization | Findings Register — Critical severity tier with the shortest SLA |
| 4 | No apparent cross-engagement pattern recognition | Repeat-finding tracking across audit cycles | Findings Register — `is_repeat` flag linking back to the originating engagement |

## Why this matters under SAMA/NCA
- **SAMA CSF 1.8** requires not just that reviews happen, but that **remediation tracking and reporting** exist as a distinct, auditable activity — the review itself is necessary but not sufficient.
- **NCA ECC 1‑8‑5 / 1‑8‑6** require documented remediation follow-up and reporting of audit findings to management — a finding that sits in a report nobody revisits does not satisfy this control, regardless of how thorough the original review was.
- The SolarWinds case is frequently cited in GRC and audit literature specifically because it illustrates that **detection is not the failure point in every major breach** — sometimes the weakness was already known, and the failure is in the follow-through.

## Discussion questions for your LinkedIn/portfolio writeup
- If your organization's last internal audit identified a Critical finding, could you say with confidence, right now, whether it's actually been remediated and verified — or just marked "in progress" indefinitely?
- Does your organization track *repeat* findings across audit cycles as their own risk signal, separate from tracking each finding individually?
- What's the review/audit equivalent of SolarWinds' build server — a piece of infrastructure whose security weakness would have disproportionate blast radius if left unaddressed?
