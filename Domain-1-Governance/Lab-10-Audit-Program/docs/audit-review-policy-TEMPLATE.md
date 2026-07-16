# Cyber Security Review &amp; Audit Policy
**Maps to:** SAMA CSF 1.8, NCA ECC 1‑8

## 1. Purpose
Ensure security weaknesses identified through review and audit activity are tracked to verified closure — not just documented and filed. Detection without follow-through is treated as equivalent to non-detection for governance purposes.

## 2. Required Assurance Activities
| Activity | Frequency |
|---|---|
| Internal cybersecurity audit | Annual minimum |
| Independent external assessment | Annual |
| Penetration testing | Annual minimum |
| Vulnerability assessment | Monthly (see Lab 03) |
| Regulatory examination | Per regulator schedule |

## 3. Remediation SLA by Severity
| Severity | Remediation SLA |
|---|---|
| Critical | 30 days |
| High | 60 days |
| Medium | 90 days |
| Low | 180 days |

Any finding on infrastructure with disproportionate blast-radius potential (e.g., build/release pipelines, core banking systems, identity providers) is treated as Critical regardless of its initial technical severity rating.

## 4. Repeat Finding Escalation
Any finding that recurs across audit cycles — the same weakness identified more than once — is automatically escalated to the CISO and reported to the Board Risk & Compliance Committee as a standing item until closed, regardless of its individual severity rating. A repeat finding indicates the remediation process itself has failed, which is a governance issue independent of the underlying technical issue.

## 5. Committee Reporting
All findings — and specifically all overdue and repeat findings — are reported to the Board Risk & Compliance Committee at each meeting. A finding that never reaches a committee agenda is treated as a reporting failure in its own right.

## 6. Review
Reviewed annually or immediately following any incident traceable to a previously identified but unremediated finding — this is the specific governance failure the 2020 SolarWinds breach illustrates.

---
*This is a plain-document policy template. The lab's app (`src/`) tracks live findings, SLAs, and committee reporting, and can generate a printable audit report at `/report`.*
