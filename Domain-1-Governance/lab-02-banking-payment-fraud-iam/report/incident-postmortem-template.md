# Incident Postmortem Report
**Incident Type:** Attempted Fraudulent Payment / Segregation-of-Duties Test
**Modeled on:** Bangladesh Bank / SWIFT Heist (February 2016)
**Report Classification:** Confidential — Internal Use Only

---

## 1. Incident Summary
| Field | Detail |
|---|---|
| Date/Time Detected | *[from audit log timestamp]* |
| Detected By | *[Fraud engine auto-flag / Checker review]* |
| Payment ID(s) | *[from SecurePay]* |
| Amount | *[SAR]* |
| Beneficiary | *[name, account, country]* |
| Status | Blocked / Rejected / Under Investigation |
| Severity | Critical / High / Medium / Low |

## 2. Timeline
| Time (UTC) | Event |
|---|---|
| | Payment created by Maker |
| | Fraud engine flagged as HIGH risk — reasons: *[list]* |
| | Checker reviewed and rejected / SoD violation attempt logged |
| | Incident closed |

*Pull this directly from the `/audit` log export.*

## 3. Root Cause Analysis
*[Which fraud rule(s) triggered? Was this a genuine fraud attempt or a false positive? What would have happened if the fraud engine and maker-checker control were not in place — walk through it the way you would explain the 2016 heist.]*

## 4. What Would Have Happened Without These Controls
*[Reference the case study: without MFA, without maker-checker, without real-time fraud detection — describe the plausible bad outcome, drawing the explicit parallel to the ~$81M that left Bangladesh Bank.]*

## 5. Controls That Worked
- [ ] MFA prevented/would have prevented unauthorized login
- [ ] Maker-checker segregation prevented single-point release
- [ ] Fraud engine flagged the transaction in real time (not after the fact)
- [ ] Audit log provided a complete, reconstructable timeline

## 6. Gaps Identified / Recommendations
| Gap | Recommendation | Owner | Target Date |
|---|---|---|---|
| | | | |

## 7. Regulatory Notification
- SAMA CSF 5.3 requires notification within 2 hours for critical incidents. Was this threshold met? *[Y/N + evidence]*
- Would this incident, if real, meet PDPL 72-hour breach notification criteria (if personal data involved)? *[assess]*

## 8. Lessons Learned
*[2-3 bullet points, written for a Board/CISO audience]*

## 9. Sign-off
| Name | Role | Date |
|---|---|---|
| | Fraud Desk / Checker | |
| | CISO | |
