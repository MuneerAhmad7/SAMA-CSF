# Segregation of Duties (SoD) Policy — Payment Systems
**Maps to:** SAMA CSF 1.4 / 3.7, NCA ECC 1‑4‑3

| Field | Value |
|---|---|
| Owner | CISO / Head of Payments Operations |
| Approved by | Board Risk & Compliance Committee |
| Scope | All systems capable of originating or approving fund transfers |

## 1. Purpose
Ensure no single individual can both **originate** and **authorize/release** a financial transaction, preventing the single-point-of-compromise scenario that enabled the 2016 Bangladesh Bank / SWIFT heist.

## 2. Mandatory Control: Maker-Checker
- Every payment instruction MUST be created by a **Maker** and approved by a **different, independently authenticated Checker**.
- The system MUST technically prevent (not just procedurally discourage) a Maker from approving their own transaction.
- Any attempted self-approval MUST be logged as a security event and escalated to the CISO.

## 3. Role Definitions
| Role | Can do | Cannot do |
|---|---|---|
| Maker | Create/draft payment instructions | Approve any payment, including their own |
| Checker | Approve or reject payments created by others | Create payments, approve own-created payments |
| Admin | Manage users/roles, view audit logs | Create or approve payments (separate function) |

## 4. Authentication Requirements
- MFA (TOTP or hardware token) mandatory for all Maker, Checker, and Admin roles.
- Session timeout after 15 minutes of inactivity for payment-system users.

## 5. Thresholds Requiring Dual Approval (example — tune to your org)
| Transaction Value (SAR) | Approvals Required |
|---|---|
| < 100,000 | 1 Checker |
| 100,000 – 5,000,000 | 1 Checker + flagged for daily fraud review |
| > 5,000,000 | 2 Checkers (dual control) + CISO/Ops Head notification |

## 6. Monitoring
- All Maker/Checker actions logged with timestamp, user, IP, and outcome.
- Daily review of flagged/high-risk transactions by fraud desk.
- Quarterly review of SoD violation attempts by Internal Audit.

## 7. Exceptions
Any deviation (e.g., emergency single-approval process) requires documented CISO approval, time-bound, and retrospective dual review within 24 hours.

## 8. Review
Reviewed annually or after any SoD-related security incident.
