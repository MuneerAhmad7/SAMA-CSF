# Case Study: The Uber Breach and Concealment (2016, disclosed 2017)

*This account is compiled from widely reported public facts about the incident, including subsequent regulatory settlements, summarized in the author's own words for educational use in this lab. It focuses on the organizational and regulatory-compliance failure, not on any individual.*

## Timeline
1. In late 2016, attackers gained access to a third-party cloud storage service used by Uber to store certain data, and obtained personal information for approximately **57 million riders and drivers**, including names, email addresses, phone numbers, and driver's license numbers for around 600,000 drivers.
2. Rather than reporting the breach to regulators and notifying affected individuals as required, **the company arranged to pay the attackers to delete the stolen data and remain silent about the incident.**
3. The breach was **not disclosed publicly for approximately one year**, becoming known in **November 2017**, under new company leadership that had since taken over.
4. Multiple U.S. state attorneys general investigated the delayed notification. In 2018, Uber reached a **$148 million multistate settlement** — at the time one of the largest data breach settlements of its kind — specifically over the failure to timely notify affected individuals and regulators, not merely over the underlying breach itself.
5. The U.S. Federal Trade Commission also took action, resulting in a settlement requiring **20 years of independent, third-party privacy and security audits**.
6. Separately, the individual most directly responsible for managing the incident response was prosecuted for obstruction of justice related to concealing the breach from the FTC, which had been actively investigating Uber's data security practices at the time.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | No tracked notification deadline for the applicable regulations | A registered obligation with a computed deadline per framework, for every incident | Incident Notification Tracker |
| 2 | Concealment decision made informally, not against a tracked, escalating clock | An independent tracker whose status doesn't depend on individual discretion | Notification status (On Time/Late/Pending) computed automatically from incident discovery time |
| 3 | ~1 year gap between discovery and disclosure | Escalation the moment a deadline is at risk | Dashboard — overdue notifications surfaced prominently, same discipline as Lab 03's vulnerability SLAs |
| 4 | Regulators found out independently, not from the company | Every notification tracked to completion, verifiable after the fact | Notification Tracker — `notified_at` timestamp required to close the obligation |

## Why this matters under SAMA/NCA/PDPL
- **SAMA CSF 5.3** requires SAMA notification **within 2 hours** for critical incidents — a deadline measured in hours, not the roughly 8,760 hours (one year) it took Uber to disclose.
- **PDPL** imposes a **72-hour breach notification requirement to SDAIA** — again, a deadline that assumes an organization is actively tracking the clock from the moment of discovery, not deciding later whether disclosure is convenient.
- **NCA ECC 1‑7** requires ongoing compliance monitoring specifically because a policy that exists on paper, without an operational mechanism forcing the clock to run, doesn't produce the outcome regulators actually need.
- The size of Uber's regulatory settlement — larger than many breach-response costs — is itself a lesson: **regulators consistently penalize concealment and delay more severely than the underlying incident**, because concealment removes their ability to protect the public in real time.

## Discussion questions for your LinkedIn/portfolio writeup
- If a Critical incident occurred at your organization today, could you state, right now, every regulatory notification deadline it would trigger — and who is tracking each one?
- Is your organization's breach-notification decision a tracked, time-bound obligation, or a judgment call made under pressure by whoever is in the room?
- What would it look like, concretely, for your organization to miss a 72-hour or 2-hour deadline by even a few hours — and does anyone currently get paged when that clock is running low?
