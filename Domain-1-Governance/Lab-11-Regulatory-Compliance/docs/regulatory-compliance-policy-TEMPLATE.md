# Regulatory Compliance Policy
**Maps to:** SAMA CSF 1.9, NCA ECC 1‑7, PDPL

## 1. Purpose
Ensure every regulatory notification obligation is tracked against a computed, time-bound deadline from the moment an incident is discovered — never left to a discretionary judgment call under pressure.

## 2. Regulatory Framework Register
Every regulation or standard that applies to the organization must be registered with:
- The specific regulator (SAMA, NCA, SDAIA, PCI Security Standards Council, SWIFT, etc.)
- Its critical-incident notification deadline, in hours
- Its scope (which systems, data, or activities it governs)
- A named accountable owner

## 3. Mandatory Notification Clock Start
The moment an incident is confirmed, **every applicable regulatory framework's notification clock starts immediately** — not after internal deliberation about severity, business impact, or whether disclosure is convenient. Determining which frameworks apply is a checklist exercise, not a judgment call.

## 4. Notification Deadlines (illustrative — confirm against current regulatory guidance)
| Framework | Regulator | Deadline |
|---|---|---|
| SAMA CSF | SAMA | 2 hours (critical incidents) |
| PDPL | SDAIA | 72 hours |
| NCA ECC | NCA | Per incident severity classification |
| PCI-DSS | PCI Security Standards Council | Per contractual/card brand requirements |
| SWIFT CSP | SWIFT | Per CSP mandatory controls |

## 5. Escalation on Approaching Deadlines
Any notification clock with less than 25% of its window remaining, unmet, is automatically escalated to the CISO. Any clock that expires without notification is escalated to the CEO and Board Risk & Compliance Committee immediately — this is a Critical governance failure independent of the underlying incident's technical severity.

## 6. Prohibition on Informal Resolution
No incident meeting a regulatory notification threshold may be resolved informally (e.g., through private arrangement with an external party) in place of formal regulatory notification. This is the specific failure mode illustrated by the 2016/2017 Uber breach concealment.

## 7. Review
Reviewed annually or immediately following any missed or late regulatory notification.

---
*This is a plain-document policy template. The lab's app (`src/`) tracks live notification clocks, compliance gaps, and regulator correspondence, and can generate a printable audit report at `/report`.*
