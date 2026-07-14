# Case Study: Bangladesh Bank / SWIFT Heist (February 2016)

*This account is compiled from widely reported public facts about the incident, summarized in the author's own words for educational use in this lab. It is not a verbatim reproduction of any single news source.*

## Timeline (general sequence of events)
1. Attackers gained access to Bangladesh Bank's internal network months ahead of the theft, reportedly through a spear-phishing / malware foothold, and eventually obtained valid credentials for the bank's SWIFT payment terminal.
2. Over a weekend (when Bangladesh's work week meant the central bank was closed while the New York Fed was open, widening the window before anyone would notice), the attackers used those credentials to issue around three dozen fraudulent payment instructions.
3. The instructions requested transfers totaling roughly **$951 million** out of Bangladesh Bank's account at the **Federal Reserve Bank of New York**, to accounts in the Philippines and Sri Lanka.
4. Most of the requests were blocked — some by the Fed's own screening, one because the beneficiary name in a Sri Lanka-bound transfer contained a spelling error that a routing bank flagged as suspicious.
5. **Roughly $81 million** was successfully transferred to accounts at Rizal Commercial Banking Corporation (RCBC) in the Philippines, quickly withdrawn, and funneled through casinos, making recovery extremely difficult.
6. The fraud was only discovered when Bangladesh Bank staff returned to the office and found the SWIFT terminal printer had run out of paper — meaning confirmation messages from the Fed had gone unnoticed for a critical stretch of time.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | Valid credentials, no second factor | Mandatory MFA on all privileged/payment terminals | TOTP enforced at login |
| 2 | One compromised identity could originate AND (functionally) get funds released | Maker-checker segregation of duties | Maker cannot approve own payment; enforced server-side |
| 3 | Large number of unusual transfers to new beneficiaries went out in a short window | Real-time transaction/fraud monitoring | Rule engine: new-beneficiary + high-value, velocity checks |
| 4 | Confirmation messages went unnoticed for hours because a printer ran out of paper | Centralized, monitored logging/alerting — not a single point of physical failure | Digital audit log + dashboard, no reliance on a single physical channel |
| 5 | Investigators had to reconstruct events after the fact from scattered records | Immutable, centralized audit trail | `AuditLog` table capturing every action with timestamp and actor |

## Why this matters under SAMA/NCA
- **SAMA CSF 3.7** explicitly names SWIFT CSP (Customer Security Programme) compliance as a required control for SAMA-regulated payment institutions — a direct regulatory response to incidents like this one.
- **SAMA CSF 5.3** requires SAMA notification within 2 hours for critical incidents — the opposite of a multi-day discovery delay.
- **NCA ECC 1‑4‑3** (segregation of duties) exists specifically to prevent one identity from having both the ability to create and to effectively execute a high-value transaction.

## Discussion questions for your LinkedIn/portfolio writeup
- If Bangladesh Bank had enforced MFA + maker-checker, at what step would this attack have failed?
- Which single control in this lab would have had the highest impact if implemented alone?
- What's the equivalent "printer ran out of paper" single point of failure in your own organization's monitoring setup?
