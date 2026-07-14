# Cloud Security Policy
**Maps to:** SAMA CSF 4.3, NCA ECC 4‑2, NCA Cloud Cybersecurity Controls (CCC)

## 1. Scope
*[Which cloud providers, accounts, and environments does this policy cover?]*

## 2. Least-Privilege IAM Requirement
- Every IAM role/user must be scoped to the minimum permissions required for its function.
- Wildcard (`*`) permissions are prohibited outside documented, time-bound exceptions approved by the CISO.
- IAM roles attached to internet-facing resources (WAFs, load balancers, API gateways) require **quarterly review** given their elevated exposure — this is the exact control gap behind the 2019 Capital One breach.

## 3. Data Storage Requirements
- All storage (S3, RDS, EBS) containing Confidential or Restricted data must have encryption at rest enabled.
- Public read/write access to storage buckets is prohibited by default; any exception requires documented business justification and CISO approval.
- Access logging must be enabled on all storage containing Confidential or Restricted data.

## 4. Network Security Requirements
- Security groups/firewall rules must not expose administrative or database ports (SSH, RDP, database ports) to 0.0.0.0/0.
- Web Application Firewalls (WAFs) protecting internet-facing applications must be reviewed for configuration drift on a defined cadence, not just at initial deployment.

## 5. Continuous Monitoring (CSPM) Requirement
- All Production cloud resources must be covered by continuous configuration monitoring.
- Non-Production environments (Staging, Development) must have a documented monitoring plan, even if less frequent than Production.
- Findings must be tracked through a defined remediation workflow with named ownership and severity-based SLAs.

## 6. Review Cycle
Reviewed annually or immediately following any cloud security incident or major architecture change.

---
*This is a plain-document policy template. The lab's app (`src/`) tracks live findings against these requirements and can generate a printable audit report at `/report`.*
