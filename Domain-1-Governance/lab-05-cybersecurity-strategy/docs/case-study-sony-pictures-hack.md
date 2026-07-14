# Case Study: The Sony Pictures Entertainment Hack (2014)

*This account is compiled from widely reported public facts about the incident, summarized in the author's own words for educational use in this lab.*

## Timeline
1. **April 2011** — Sony's PlayStation Network suffers a massive breach, exposing personal data for roughly 77 million user accounts, at the time one of the largest breaches ever disclosed. The incident drew heavy public and regulatory scrutiny over Sony's security posture.
2. Over the following years, Sony Pictures Entertainment — a related but organizationally distinct part of the wider Sony group — continued operating with security practices that, in hindsight commentary following the 2014 incident, were widely characterized as underfunded relative to the risk the studio faced.
3. **Late November 2014** — A group calling itself "Guardians of Peace" breaches Sony Pictures' network. Attackers deploy destructive wiper malware that disables large numbers of workstations and servers across the studio.
4. Attackers leak a large volume of internal data: unreleased films, confidential financial data, and particularly damaging **internal executive emails** containing candid, unflattering communications that generated significant media coverage and reputational harm.
5. Personal data belonging to thousands of current and former employees, including Social Security numbers and salary information, is also exposed.
6. The attack is widely attributed by U.S. authorities to North Korea, linked to Sony Pictures' upcoming release of a comedy film depicting the assassination of North Korea's leader — a **geopolitically foreseeable trigger** that, in retrospect, should have informed a heightened defensive posture ahead of the film's release.
7. Post-incident commentary and reporting emphasized a recurring theme: despite the scale of the 2011 PSN breach three years earlier, Sony Pictures' security program had not undergone the kind of sustained, strategic, board-funded transformation that would have meaningfully raised its resilience against a well-resourced, motivated adversary.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | No sustained multi-year security strategy despite a major prior breach | Documented 3-5 year strategy, reviewed and re-funded annually | Strategy Builder — Strategic Period + Review Cycle fields |
| 2 | Security treated as reactive cost center | Budget formally tied to strategic priorities, tracked over time | Strategic Roadmap — budget allocated/spent per initiative |
| 3 | A known geopolitical trigger (the film's release) wasn't reflected in elevated posture | Living threat-landscape assessment feeding strategic priorities | Threat Landscape Register, including nation-state/geopolitical category |
| 4 | Lessons from 2011 didn't produce lasting strategic change | KPIs/KRIs tracking maturity improvement over time | Maturity Assessment — current vs. target level per domain |
| 5 | No clear roadmap connecting current state to target maturity | Phased roadmap with owners and budgets | Strategic Roadmap — Foundation/Core/Advanced/Optimization phases |

## Why this matters under SAMA/NCA
- **SAMA CSF 1.2** requires a 3-5 year cybersecurity strategy aligned with business strategy, reviewed annually, with budget allocation and KPIs/KRIs — precisely the sustained, funded approach that was reportedly missing at Sony Pictures.
- **NCA ECC 1‑1** requires the strategy to be formally approved by the organization's head, communicated to stakeholders, and reviewed periodically — not a document that exists once and is never revisited as the threat landscape shifts.
- The **SAMA CSF maturity model (Level 0–5)** exists specifically to make "are we actually getting better over time" measurable — the gap this case illustrates so clearly.

## Discussion questions for your LinkedIn/portfolio writeup
- If your organization suffered a major breach today, what would you point to as evidence that the *strategy*, not just individual controls, changed afterward?
- Does your organization's threat landscape assessment account for foreseeable geopolitical or reputational triggers specific to your business (a controversial product launch, a high-profile deal, a public dispute)?
- What's the difference between "we fixed the vulnerability that caused the last breach" and "we have a strategy that would have prevented the *next* one"?
