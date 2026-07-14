# Payment Authorization Matrix
**Maps to:** SAMA CSF 3.7, NCA ECC 2‑2

| Transaction Type | Maker | Checker(s) Required | MFA Required | Additional Control |
|---|---|---|---|---|
| Domestic transfer < 100K SAR | Operations Staff | 1 | Yes | Standard fraud rules |
| Domestic transfer 100K–5M SAR | Operations Staff | 1 | Yes | Fraud engine review + new-beneficiary flag |
| Domestic transfer > 5M SAR | Senior Operations | 2 (dual control) | Yes | CISO/Ops Head notified, 24h cooling-off for new beneficiary |
| International / SWIFT transfer (any value) | Senior Operations | 2 (dual control) | Yes (hardware token preferred) | High-risk country screening, correspondent bank verification |
| New beneficiary (any channel) | Operations Staff | 1 + fraud desk review | Yes | 24h hold recommended for first transaction |
| Off-hours submission | Operations Staff | Escalated Checker (on-call) | Yes | Auto-flagged, requires justification note |

## High-Risk Destination Watchlist (example structure — populate per your compliance/AML team)
Maintain a list of jurisdictions requiring enhanced due diligence per SAMA AML guidance and FATF lists. Do not hardcode political judgments into engineering docs — reference the compliance team's official, regularly updated list.

## Escalation
Any transaction flagged by 2+ fraud rules simultaneously is automatically routed to the CISO/Fraud Desk regardless of value, per this lab's `fraud_engine.py` logic.
