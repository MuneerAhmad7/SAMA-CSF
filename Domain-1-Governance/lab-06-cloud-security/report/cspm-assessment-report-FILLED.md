# Cloud Security Posture Assessment Report
**Organization:** Falak Pay Financial Company (fictional entity, lab use)
**Assessment Date:** *[generated from seeded demo data]*
**Maps to:** SAMA CSF 4.3, NCA ECC 4‑2 | **Classification:** Confidential — Internal Use Only

---

## 1. Executive Summary
Falak Pay's Cloud Security Posture Score is **32/100** — a score reflecting real, unresolved risk that requires immediate remediation focus. Of 14 tracked findings across 12 cloud resources, the most critical is a **direct replay of the 2019 Capital One breach pattern**: an IAM role (`waf-service-role`) attached to a public-facing WAF with S3 permissions far broader than the WAF requires.

Four Critical findings remain open or in investigation. Given the sensitivity of the affected resources (customer data, payment logs, and the WAF/IAM combination itself), this assessment recommends treating IAM least-privilege remediation as the top organizational priority this cycle.

## 2. Scope & Methodology
- **Scope:** 12 cloud resources (S3 buckets, IAM roles, security groups, WAF ACLs, RDS, EC2) across Production, Staging, and Development
- **Reference case:** Capital One, disclosed 2019 — used as the structural benchmark for IAM/WAF misconfiguration risk
- **Tooling:** Cloud Security Posture Manager (this lab's application)

## 3. Key Metrics
| Metric | Value |
|---|---|
| Cloud Security Posture Score | 32 / 100 |
| Total findings | 14 |
| Open/Investigating findings | 10 |
| Open Critical findings | 4 |
| Cloud resources tracked | 12 |
| Production resources | 9 |

## 4. Critical Finding — Capital One Pattern Replay

### Finding: IAM Role Attached to Public-Facing Resource with Excessive S3 Access (CSPM-05)
- **Resource:** `waf-service-role`, attached to `customer-portal-waf` (internet-facing)
- **Status:** Open
- **Risk:** This role currently has `s3:ListBucket` and `s3:GetObject` on **all buckets in the account**, not scoped to what the WAF actually needs. This is the exact pattern that allowed the Capital One attacker, after exploiting an SSRF vulnerability in a misconfigured WAF, to retrieve IAM credentials with far more permission than necessary and exfiltrate data from over 700 S3 buckets.
- **Recommendation:** Immediately scope this role's policy to the specific bucket ARNs the WAF requires, removing wildcard/account-wide S3 access. Treat as emergency change given the resource's Critical sensitivity rating.

### Related Finding: IAM Role with Wildcard Permissions (CSPM-04)
- Also present on `waf-service-role` — a leftover wildcard (`Action: "*"`, `Resource: "*"`) statement from initial testing that was never scoped down. This compounds the CSPM-05 risk and should be remediated in the same change.

### Related Finding: WAF Misconfiguration Enabling SSRF-Style Requests (CSPM-07)
- Currently in Investigating status. The WAF rule set has a gap potentially allowing SSRF-style request patterns through to backend metadata endpoints — the exact technique used in the Capital One attack to retrieve the over-permissioned role's credentials in the first place.

## 5. Other Notable Findings
| Finding | Resource | Severity | Status |
|---|---|---|---|
| S3 bucket allows public-read (legacy migration script) | backup-vault-s3 | High | Open |
| Missing encryption at rest on payment transaction logs | payment-logs-prod-s3 | Medium | Open |
| MFA not enforced on IAM user | app-backend-role | High | Open |
| Database port open to 0.0.0.0/0 | payments-api-sg | High | Open |
| No CSPM coverage of Development environment | dev-sandbox-s3 | High | Open |

## 6. Well-Managed Examples (for contrast)
- **customer-data-prod-s3** access logging gap — remediated, pending final verification.
- **staging-app-ec2** SSH exposure — remediated, restricted to VPN CIDR.
- **core-banking-db** encryption — verified, using a customer-managed KMS key.

These demonstrate the remediation workflow functioning correctly when findings are actively worked.

## 7. Root Cause Themes
1. **IAM permissions granted broader than needed "to be safe," never scoped down** — the single highest-risk pattern in this assessment, directly mirroring Capital One.
2. **CSPM coverage gap in non-Production environments** — Development is currently unmonitored, meaning misconfigurations there could persist indefinitely undetected.
3. **Legacy artifacts from migrations/testing left in place** — both the public-read S3 ACL and the wildcard IAM policy trace back to setup activity that was never cleaned up.

## 8. Recommendations & Roadmap
| Priority | Action | Owner | Target Date |
|---|---|---|---|
| P1 | Scope waf-service-role to specific bucket ARNs; remove wildcard permissions | Omar Al-Shammari | Within 48 hours |
| P1 | Close the WAF SSRF-pattern gap | Omar Al-Shammari | Within 48 hours |
| P2 | Remove public-read ACL from backup-vault-s3 | Fatimah Al-Zahrani | Within 1 week |
| P2 | Enable encryption at rest on payment-logs-prod-s3 | Fatimah Al-Zahrani | Within 1 week |
| P2 | Restrict payments-api-sg database port to application subnet only | Omar Al-Shammari | Within 1 week |
| P3 | Extend CSPM coverage to Development environment | Layla Al-Ghamdi | Next quarter |

## 9. Conclusion
Falak Pay's cloud environment currently carries the same structural risk pattern that caused the Capital One breach — an over-permissioned IAM role attached to a public-facing control. Unlike Capital One, this risk is visible and tracked in this register rather than undiscovered; the immediate priority is closing it before it becomes exploitable rather than after.

## 10. Sign-off
| Name | Role | Date |
|---|---|---|
| Khalid Al-Mutairi | CISO | |
| Board Risk & Compliance Committee Chair | | |

---
*This report was generated against the seeded demo dataset in this lab (`seed_demo_data.py`). Regenerate the live version anytime via the app's `/report` view.*
