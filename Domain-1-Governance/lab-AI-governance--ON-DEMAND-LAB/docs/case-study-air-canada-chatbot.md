# Case Study: The Air Canada Chatbot Ruling (2022–2024)

*This account is compiled from widely reported public facts about the incident, including the published tribunal decision, summarized in the author's own words for educational use in this lab.*

## Timeline
1. In November 2022, a customer visited Air Canada's website following a family member's death and used the airline's website chatbot to ask about bereavement fares.
2. The chatbot told the customer he could book a flight at the regular price and **apply for a bereavement discount retroactively**, within 90 days of the ticket date.
3. This advice **did not reflect Air Canada's actual bereavement policy**, which required the discount to be requested before travel, not claimed afterward.
4. The customer booked accordingly, then attempted to claim the promised retroactive discount. Air Canada refused, pointing to its actual written policy.
5. The customer took the case to the British Columbia Civil Resolution Tribunal. Air Canada's defense reportedly argued that **the chatbot was a separate entity "responsible for its own actions,"** and that the airline should not be liable for what it said.
6. In February 2024, the tribunal **rejected that argument**, ruling that Air Canada was responsible for all information on its website, including information provided by a chatbot, and ordered the airline to pay damages reflecting the difference the customer was promised.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | No human-in-the-loop checkpoint for policy-sensitive topics (refunds, exceptions, bereavement) | A defined, enforced escalation trigger for specific topic categories | Oversight Checkpoints module — per-system, per-trigger, with an enforced/not-enforced flag |
| 2 | No apparent process sampling chatbot answers against real policy | Periodic statistical review of outputs against a rubric | Output Sample Review Log — rolling accuracy %, not a one-time test |
| 3 | No clear accountability — the company's own defense denied ownership of the AI's statements | A named model owner and an incident process treating AI errors like any other customer-facing failure | Incident Log — AI Systems have owners, and failures are tracked Open → Resolved with root cause |
| 4 | No visible change-control narrative for how the chatbot's content/behavior was managed | Version-controlled, approved changes to model/prompt/guardrail configuration | Model Change Log — Pending/Approved/Rejected status per change |

## Why this matters for governance evidence (not a specific SAMA/NCA citation)
Neither SAMA CSF nor NCA ECC, as published, define a dedicated AI/LLM control domain — this case predates and sits outside their explicit scope. But the underlying GRC principles both frameworks *do* require — governance strategy covering emerging technology, human sign-off on sensitive decisions, incident tracking, and change control — apply just as much to a chatbot as to a payment system. The practical problem, and the one this lab is built to solve, is: **what does the evidence look like when the system's output isn't the same every time you check it?**

The answer this lab implements: you don't evidence a single output. You evidence a **process** — sampling, trending, escalation enforcement, and incident handling — the same way a Board doesn't review every transaction a bank processes, but does review the sampled audit and control-testing results that stand in for full coverage.

## Discussion questions for your LinkedIn/portfolio writeup
- If your organization deployed a customer-facing chatbot today, could you produce, on demand, a sampled accuracy rate for its answers on your most sensitive policy topics — or would the honest answer be "we haven't checked"?
- Is there a named, accountable owner for each AI system in your environment, the way there's a named owner for a server or a database?
- What's your organization's equivalent of Air Canada's legal argument — a place where an AI system's output isn't yet clearly anyone's responsibility?
