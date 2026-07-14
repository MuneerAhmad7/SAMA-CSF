# Case Study: The British Airways Breach (2018)

*This account is compiled from widely reported public facts about the incident, summarized in the author's own words for educational use in this lab.*

## Timeline
1. Sometime before August 21, 2018, attackers gained the ability to modify code running on British Airways' website and mobile app checkout flow.
2. Attackers injected malicious JavaScript into the **payment page** — a technique publicly documented as consistent with the "Magecart" family of attacks, where a script silently captures form data (card number, expiry, CVV, billing details) as a customer types it, and transmits a copy to an attacker-controlled server, while the actual transaction proceeds normally so nothing appears wrong to the customer.
3. The malicious script ran for approximately **two and a half weeks**, from around August 21 to September 5, 2018, before British Airways identified and removed it.
4. The breach exposed personal and payment card data for approximately **380,000 customer transactions**.
5. The UK's Information Commissioner's Office (ICO) investigated and proposed a substantial fine under GDPR, one of the largest of its kind at the time, later reduced on appeal but still highly significant — reflecting regulatory view of the severity of the control failures involved.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | A code change reached the live payment page without rigorous security review | Documented security sign-off (Deploy gate) required before go-live | Security Gate Checklist — Deploy gate, named approver required |
| 2 | No integrity control on scripts running on the payment page | Third-party script/code integrity register with SRI hashing | Third-Party Script Register — SRI-pinned tracking |
| 3 | Malicious script ran undetected for ~2.5 weeks | Continuous monitoring for unauthorized changes to customer-facing pages | Change Record — flags any change without a passed Deploy gate |
| 4 | No apparent threat modeling specific to the payment flow | Security requirements defined at project Initiation | Security Gate Checklist — Initiation gate |

## Why this matters under SAMA/NCA
- **SAMA CSF 1.5** explicitly requires: security requirements in all project charters, security gate reviews at each project phase, threat modeling for new systems, and **security sign-off before go-live** — every one of which, if rigorously enforced, targets exactly this kind of failure.
- **NCA ECC 2‑8** (Secure Software Development) requires secure coding standards, code review (manual and automated), and controlled, change-managed deployment — the direct technical counterpart to "a script reached production without anyone verifying what it did."
- A payment page is about as sensitive a piece of customer-facing code as exists in a financial services context — which is exactly why this lab treats "Deploy gate not passed" as a flagged, visible finding rather than a footnote.

## Discussion questions for your LinkedIn/portfolio writeup
- If a developer pushed a change to your organization's payment or login page tomorrow, would it be technically possible for that change to reach production without a security sign-off — or is that gate actually enforced, not just documented?
- Do you currently have a list of every third-party script running on your most sensitive customer-facing pages, and whether each one is integrity-verified?
- How would your organization detect an unauthorized change to a payment page within hours, rather than weeks?
