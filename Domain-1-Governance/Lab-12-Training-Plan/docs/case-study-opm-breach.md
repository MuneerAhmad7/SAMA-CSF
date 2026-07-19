# Case Study: The OPM Breach (Discovered 2015)

*This account is compiled from widely reported public facts about the incident, including the subsequent U.S. congressional oversight report, summarized in the author's own words for educational use in this lab.*

## Timeline
1. Between approximately 2014 and 2015, attackers gained access to systems belonging to the U.S. Office of Personnel Management (OPM), the federal agency responsible for, among other things, conducting background investigations for security clearances.
2. The attackers exfiltrated records for **over 21 million people**, including current and former federal employees, contractors, and — because background investigations cover associates and family members — many people who had never worked for the government at all. Some of the stolen data included highly sensitive background-investigation material (the kind of detailed personal history submitted on security clearance forms), and for a large subset, fingerprint data.
3. The intrusion was discovered in **2015**, though evidence suggested attacker presence for a significant period before detection.
4. A subsequent U.S. congressional oversight investigation produced a detailed report examining how the breach happened. A central theme of that report was that **OPM's own Inspector General had issued repeated audit findings over preceding years documenting serious weaknesses in the agency's technical security capability and practices** — findings that, in the committee's assessment, had not been adequately acted upon.
5. The report characterized the breach not as the result of a single sophisticated, unstoppable technique, but as the culmination of **long-documented, known technical capability gaps** that persisted despite repeated warnings.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | Repeated audit findings about technical capability, not acted on | A tracked training needs assessment tied to specific, named skill gaps | Skills Matrix — current vs. required competency by specialty |
| 2 | No systematic tracking of staff certifications against role requirements | A certification register with expiry monitoring | Certification Register — Active/Expiring Soon/Expired status |
| 3 | Security staff depth not matched to the sensitivity of systems protected | A skills matrix reflecting required competency level per role/specialty | Skills Matrix — required_level field, gap = required minus current |
| 4 | Training treated as a checkbox rather than a funded program | A budgeted, dated training plan with tracked completion | Training Plan module |

## Why this matters under SAMA/NCA
- **SAMA CSF 1.7** requires an **annual training needs assessment** — not a one-time exercise, but a recurring process specifically designed to catch a gap like OPM's before it becomes a multi-year, unaddressed weakness.
- **SAMA CSF 1.7** also requires **certification requirements** for security staff and **training records maintenance** — both of which, if systematically tracked, turn "we know we have a gap" into "here is the funded plan and target date to close it," rather than a repeated audit finding that never changes status.
- The OPM case is frequently cited in security workforce and training literature specifically because it demonstrates that **awareness training for the general workforce and technical training for the security team are different obligations with different failure modes** — this lab exists because Lab 09 (general awareness) does not, by itself, satisfy this deeper requirement.

## Discussion questions for your LinkedIn/portfolio writeup
- If your organization's last internal audit (see Lab 11) flagged a technical capability gap on the security team, is there a funded, dated training plan item addressing it — or does the finding just get re-reported next cycle?
- Are your security team's certifications tracked centrally with expiry alerts, the way a domain certificate or a software license would be?
- Does your organization's training needs assessment identify specific, named skill gaps by specialty — or is it a generic "complete your annual training" reminder?
