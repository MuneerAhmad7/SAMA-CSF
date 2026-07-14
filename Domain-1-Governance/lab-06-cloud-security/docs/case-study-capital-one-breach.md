# Case Study: The Capital One Breach (2019)

*This account is compiled from widely reported public facts about the incident, summarized in the author's own words for educational use in this lab.*

## Timeline
1. Capital One, like many large financial institutions, hosted web applications and data in the AWS cloud, using a Web Application Firewall (WAF) to protect internet-facing applications.
2. A former employee of a cloud computing company discovered that the WAF was **misconfigured in a way that made it vulnerable to Server-Side Request Forgery (SSRF)** — a technique that tricks a server into making requests on the attacker's behalf.
3. Using this SSRF weakness, the attacker caused the WAF to query **AWS's internal instance metadata service**, which (when reachable) returns temporary security credentials for whatever IAM role is attached to that instance.
4. The IAM role attached to the WAF had been granted **permissions far beyond what a WAF needs to function** — critically, the ability to list and read a large number of S3 storage buckets across the organization's AWS environment.
5. Using the stolen temporary credentials, the attacker enumerated and downloaded data from **over 700 S3 buckets**.
6. The breach exposed personal information for approximately **106 million individuals** in the US and Canada, including names, addresses, credit scores, credit limits, balances, and — for a smaller subset — Social Security numbers and linked bank account numbers.
7. The activity was discovered after the attacker discussed it publicly online; Capital One was notified and disclosed the breach in July 2019.

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | WAF misconfigured, vulnerable to SSRF | Regular configuration review of internet-facing controls | Findings Register — CSPM-07 (WAF misconfiguration checks) |
| 2 | IAM role attached to the WAF had excessive S3 permissions | Least-privilege IAM policy review | CSPM-04, CSPM-05 — the direct replay finding in this lab |
| 3 | No effective detection of large-scale, unusual S3 access | Continuous monitoring / anomaly detection on data access | CSPM-03, CSPM-10 (logging and continuous monitoring findings) |
| 4 | Misconfiguration existed for an extended period undetected internally | Continuous CSPM scanning, not a one-time review | This lab's entire Findings Register model |

## Why this matters under SAMA/NCA
- **SAMA CSF 4.3** requires a documented cloud security architecture review and ongoing cloud provider assessment — precisely the kind of review that should catch an over-permissioned IAM role before it becomes exploitable.
- **NCA ECC 4‑2** and the **NCA Cloud Cybersecurity Controls (CCC)** require cloud IAM to follow least-privilege principles and require continuous cloud security posture monitoring, not a point-in-time assessment at initial deployment.
- The **CIS AWS Foundations Benchmark** (an industry-standard reference, not a Saudi regulation, but commonly used alongside SAMA/NCA controls) explicitly flags wildcard IAM permissions and public S3 bucket access as high-severity findings — both represented in this lab's rule set.

## Discussion questions for your LinkedIn/portfolio writeup
- If your organization's cloud IAM roles were audited today, how confident are you that each one follows least privilege — or would some, like Capital One's WAF role, have permissions "just in case"?
- Is cloud configuration reviewed continuously in your environment, or only at the point a resource is first deployed?
- What's the blast radius if a single over-permissioned role in your cloud environment were compromised tomorrow?
