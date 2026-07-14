# Policy Framework Overview
**Maps to:** SAMA CSF 1.3, NCA ECC 1‑3

## 1. Hierarchy Structure
```
Master Policy (Board-approved, enterprise-wide)
  └── Domain Policies (one per control domain)
        └── Standards (technical requirements within a domain)
        └── Procedures (step-by-step operational instructions)
```

## 2. Required Control Domains
| Domain | Policy Owner | Status |
|---|---|---|
| Governance | | |
| Identity & Access Management | | |
| Data Protection | | |
| Cryptography | | |
| Incident Response | | |
| Business Continuity | | |
| Third-Party & M&A Security | | |
| Human Resources Security | | |
| Physical Security | | |
| Cloud Security | | |
| Security Awareness & Training | | |

## 3. Review Cycle
All policies reviewed at minimum annually, or immediately following:
- A major security incident
- A merger, acquisition, or divestiture
- A significant regulatory change (SAMA/NCA/SDAIA)

## 4. M&A / Third-Entity Integration Requirement
Any newly acquired entity or new third-party relationship must have a documented plan for extending this policy framework to their systems, with a **named owner and hard deadline** — not an open-ended "eventually." See the M&A / Third-Entity Integration Register for live tracking.

---
*This is a plain-document overview for reference or offline editing. The lab's app (`src/`) builds and tracks this framework interactively and can generate a live, printable version at `/report`.*
