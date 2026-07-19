# Security Team Technical Training &amp; Certification Policy
**Deepens:** SAMA CSF 1.7

## 1. Purpose
Ensure the technical security function maintains the certifications and skill depth required for its role — a distinct, deeper obligation from general staff awareness training (see the organization's Awareness &amp; Training Policy).

## 2. Skills Matrix Requirement
Every technical security team member is assessed at least annually against a defined set of specialties (e.g., Incident Response, Cloud Security, Digital Forensics, Penetration Testing, GRC/Audit, Secure Code Review), with:
- A current competency level (0–4)
- A required competency level for their specific role
- Any gap tracked to a named, funded training plan item — not left as a standalone finding

## 3. Certification Requirements
- Role-required certifications are documented per position (e.g., CISSP for CISO/senior leadership, relevant GIAC/OSCP/CCSP credentials for specialist roles).
- Certification expiry is tracked centrally with automated flagging: Active, Expiring Soon (within 90 days), or Expired.
- **An expired required certification for an active role is treated as a compliance gap requiring immediate remediation planning**, not merely a renewal reminder.

## 4. Training Needs Assessment
Conducted at minimum annually, and explicitly whenever:
- An internal or external audit (see the Audit &amp; Review Policy) identifies a technical capability gap on the security team
- A new threat category or technology adoption (e.g., cloud migration, new AI tooling) creates a new required specialty

Any gap identified through this process must result in a training plan item with a named owner, budget, and target date within one review cycle — **an identified gap without a funded plan item is itself treated as a governance finding**, per the lesson of the 2015 OPM breach.

## 5. Single-Person Concentration Risk
Where a critical specialty (e.g., Digital Forensics) is held at required depth by only one team member, this is tracked as a business-continuity risk and addressed through cross-training, not treated as sufficiently covered.

## 6. Review
Reviewed annually or immediately following any incident where response was hampered by a technical capability gap.

---
*This is a plain-document policy template. The lab's app (`src/`) tracks live skills matrices, certification expiry, and a funded training plan, and can generate a printable audit report at `/report`.*
