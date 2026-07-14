# Security in Project Management Policy
**Maps to:** SAMA CSF 1.5, NCA ECC 1‑6, 2‑8

## 1. Purpose
Ensure security requirements, review, and sign-off are built into every project's delivery lifecycle — not bolted on after the fact or skipped under deadline pressure.

## 2. Mandatory Security Gates
Every project, regardless of size, passes through 6 gates before completion:

| Gate | Requirement |
|---|---|
| Initiation | Security requirements documented; threat model started for Critical/High projects |
| Design | Threat model completed; architecture reviewed for security implications |
| Build | Secure coding standards followed; code review completed |
| Test | Security testing completed (SAST/DAST minimum; pentest for Critical projects) |
| Deploy | **Named security sign-off obtained before go-live — this gate may not be skipped or informally waived for Critical/High criticality projects** |
| Post-Implementation | Post-launch security review completed within a defined window |

## 3. On Gate Waivers
A gate may only be marked "Waived" with:
- Documented business justification
- CISO approval
- A defined, time-bound remediation plan to close the gap

**A Waived Deploy gate on a Critical, customer-facing project is treated as a reportable governance exception**, escalated to the Cyber Security Committee — this is the exact structural gap behind the 2018 British Airways breach.

## 4. Third-Party Script / Code Integrity Requirements
- Every script running on a customer-facing page must be recorded in the Third-Party Script Register.
- Scripts on Critical/High-risk pages (payment, login, checkout) must have Subresource Integrity (SRI) hashes pinned.
- Scripts must be re-reviewed at least every 6 months, or immediately following any reported vulnerability in the script or its provider.

## 5. Change Management
- No production change to a Critical/High-criticality, customer-facing system may deploy without its Deploy gate showing Passed status.
- Emergency changes require a documented, time-bound exception process distinct from a routine gate waiver, with retrospective review within 24 hours.

## 6. Review
Reviewed annually or immediately following any project-security-related incident.

---
*This is a plain-document policy template. The lab's app (`src/`) tracks live gate status per project and can generate a printable audit report at `/report`.*
