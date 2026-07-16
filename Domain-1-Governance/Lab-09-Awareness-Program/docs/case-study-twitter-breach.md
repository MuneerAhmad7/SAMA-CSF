# Case Study: The Twitter Breach (July 2020)

*This account is compiled from widely reported public facts about the incident, summarized in the author's own words for educational use in this lab.*

## Timeline
1. In mid-July 2020, attackers conducted a **phone-based social engineering ("vishing") campaign** targeting Twitter employees, reportedly impersonating IT support staff.
2. Through these calls, attackers convinced a number of employees to provide credentials or otherwise assist in accessing an **internal administrative/support tool** used by Twitter's support teams.
3. Using this access, attackers took control of **dozens of high-profile, verified Twitter accounts**, including accounts belonging to prominent political figures, celebrities, and major companies.
4. The compromised accounts were used to post messages promoting a **cryptocurrency scam**, directing followers to send funds to attacker-controlled wallets.
5. Twitter responded by temporarily **restricting the ability of all verified accounts to tweet** while investigating the scope of the compromise — an extraordinary platform-wide response reflecting how serious the access level obtained was.
6. Subsequent public reporting (including regulatory review) emphasized that the attack succeeded primarily through **social engineering of employees**, not a purely technical exploit — and that individuals with access to sensitive internal tools were specifically targeted.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | Employees provided credentials/access over the phone to a caller impersonating IT support | Vishing-specific awareness training, not just email phishing training | Dedicated "Vishing &amp; Social Engineering Awareness" course in the Training Catalog |
| 2 | No apparent identity-verification step for "IT support" requests | A documented, trained-on verification procedure regardless of contact channel | Course content requirement — see policy template |
| 3 | Privileged/support-tool access wasn't specially hardened against social engineering | Role-based awareness training for employees with sensitive access | Course `audience` targeting for privileged/IT roles |
| 4 | No evidence of regular phone-based social engineering testing | Simulation campaigns across multiple channels, not just email | Simulation Campaigns module — Vishing campaign type |

## Why this matters under SAMA/NCA
- **SAMA CSF 1.6** requires phishing simulation exercises at least quarterly — this lab treats "phishing" broadly, explicitly including vishing, because the channel doesn't change the underlying control need: can an employee recognize and resist a social engineering attempt.
- **NCA ECC 1‑10** requires measurement of awareness program effectiveness — a program that only tracks "did they watch the video" without testing real-world resistance to social engineering isn't actually measuring what matters.
- Financial institutions are a natural target for vishing specifically, given the direct path from "convince an employee" to "move money or access customer data" — making this control gap especially relevant under SAMA's mandate.

## Discussion questions for your LinkedIn/portfolio writeup
- Does your organization's awareness program test phone-based social engineering, or only email phishing?
- If someone called your organization's IT help desk today claiming to be a senior executive locked out of an account, what's the actual verification step — and would every help desk employee follow it under pressure?
- Are employees with access to sensitive internal tools (like Twitter's support tool) given additional, targeted awareness training beyond the general annual program?
