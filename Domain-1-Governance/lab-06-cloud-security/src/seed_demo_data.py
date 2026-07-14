"""
Seed demo data for the Cloud Security Posture Manager (Lab 07).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec cspm python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
import app as a

RESOURCES = [
    ("customer-portal-waf", "WAF ACL", "Production", "Omar Al-Shammari", "Critical", "arn:aws:wafv2:me-south-1:falakpay:webacl/customer-portal-waf"),
    ("customer-data-prod-s3", "S3 Bucket", "Production", "Fatimah Al-Zahrani", "Critical", "arn:aws:s3:::falakpay-customer-data-prod"),
    ("payment-logs-prod-s3", "S3 Bucket", "Production", "Fatimah Al-Zahrani", "Critical", "arn:aws:s3:::falakpay-payment-logs-prod"),
    ("waf-service-role", "IAM Role", "Production", "Omar Al-Shammari", "Critical", "arn:aws:iam::falakpay:role/waf-service-role"),
    ("app-backend-role", "IAM Role", "Production", "Layla Al-Ghamdi", "High", "arn:aws:iam::falakpay:role/app-backend-role"),
    ("core-banking-db", "RDS Instance", "Production", "Fatimah Al-Zahrani", "Critical", "arn:aws:rds:me-south-1:falakpay:db:core-banking-prod"),
    ("payments-api-sg", "Security Group", "Production", "Omar Al-Shammari", "High", "sg-0a1b2c3d4e5f"),
    ("marketing-site-s3", "S3 Bucket", "Production", "Layla Al-Ghamdi", "Low", "arn:aws:s3:::falakpay-marketing-site"),
    ("staging-app-ec2", "EC2 Instance", "Staging", "Omar Al-Shammari", "Medium", "i-0staging0123456789"),
    ("dev-sandbox-s3", "S3 Bucket", "Development", "Layla Al-Ghamdi", "Low", "arn:aws:s3:::falakpay-dev-sandbox"),
    ("analytics-role", "IAM Role", "Production", "Fatimah Al-Zahrani", "Medium", "arn:aws:iam::falakpay:role/analytics-readonly"),
    ("backup-vault-s3", "S3 Bucket", "Production", "Omar Al-Shammari", "Critical", "arn:aws:s3:::falakpay-backup-vault"),
]

# (rule_id, resource_name, status, owner, extra_description)
FINDINGS = [
    # --- THE CAPITAL ONE REPLAY: Critical, IAM role attached to public-facing WAF with excessive S3 access ---
    ("CSPM-05", "waf-service-role", "Open", "Omar Al-Shammari",
     "waf-service-role is attached to customer-portal-waf (internet-facing) and currently has s3:ListBucket "
     "and s3:GetObject on ALL buckets in the account, not scoped to what the WAF actually needs. This is the "
     "exact IAM/WAF pattern behind the 2019 Capital One breach — see docs/case-study-capital-one-breach.md."),

    ("CSPM-04", "waf-service-role", "Open", "Omar Al-Shammari",
     "Role policy includes a wildcard statement (Action: '*', Resource: '*') left over from initial testing, never scoped down."),

    ("CSPM-07", "customer-portal-waf", "Investigating", "Omar Al-Shammari",
     "WAF rule set has a gap allowing certain SSRF-style request patterns through to backend metadata endpoints; patch scheduled."),

    # --- S3 findings ---
    ("CSPM-01", "backup-vault-s3", "Open", "Fatimah Al-Zahrani",
     "Bucket ACL allows public-read on a subset of objects due to a legacy migration script; needs immediate lockdown."),

    ("CSPM-02", "payment-logs-prod-s3", "Open", "Fatimah Al-Zahrani",
     "Server-side encryption not enabled on this bucket despite containing payment transaction logs."),

    ("CSPM-03", "customer-data-prod-s3", "Remediated", "Fatimah Al-Zahrani",
     "Access logging was missing, now enabled and shipping to the central logging account. Pending final verification."),

    ("CSPM-02", "marketing-site-s3", "Verified", "Layla Al-Ghamdi",
     "Low-sensitivity static site bucket, encryption enabled and verified — included to show a clean example."),

    # --- IAM / access findings ---
    ("CSPM-08", "app-backend-role", "Open", "Layla Al-Ghamdi",
     "Underlying IAM user used for local development against this role does not have MFA enforced."),

    ("CSPM-04", "analytics-role", "Investigating", "Fatimah Al-Zahrani",
     "Read-only analytics role has broader S3 read access than the specific reporting buckets it needs; scoping in progress."),

    # --- Network findings ---
    ("CSPM-06", "payments-api-sg", "Open", "Omar Al-Shammari",
     "Security group allows inbound traffic on port 5432 (database) from 0.0.0.0/0 instead of restricting to the application subnet."),

    ("CSPM-06", "staging-app-ec2", "Remediated", "Omar Al-Shammari",
     "SSH (22) was open to 0.0.0.0/0 on the staging instance; restricted to the corporate VPN CIDR range."),

    # --- Storage encryption ---
    ("CSPM-09", "core-banking-db", "Verified", "Fatimah Al-Zahrani",
     "RDS storage encryption confirmed enabled with a customer-managed KMS key — clean finding, included for completeness."),

    # --- Monitoring meta-finding ---
    ("CSPM-10", "dev-sandbox-s3", "Open", "Layla Al-Ghamdi",
     "No CSPM/continuous configuration monitoring tool currently covers the Development environment — only Production is scanned today."),

    ("CSPM-01", "dev-sandbox-s3", "Investigating", "Layla Al-Ghamdi",
     "Bucket policy under review after the above monitoring gap was identified; possible public-read misconfiguration suspected but not yet confirmed."),
]


def get_or_create_resource(name, rtype, env, owner, sensitivity, identifier):
    existing = a.CloudResource.query.filter_by(name=name).first()
    if existing:
        return existing, False
    r = a.CloudResource(name=name, resource_type=rtype, environment=env, owner=owner,
                         sensitivity=sensitivity, identifier=identifier)
    a.db.session.add(r)
    a.db.session.commit()
    return r, True


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding Cloud Resource Inventory for Falak Pay Financial Company")
        print("=" * 70)
        resource_map = {}
        for name, rtype, env, owner, sensitivity, identifier in RESOURCES:
            r, created = get_or_create_resource(name, rtype, env, owner, sensitivity, identifier)
            resource_map[name] = r
            print(f"  [{'CREATED' if created else 'exists'}] {name} ({env}, {sensitivity})")

        print()
        print("=" * 70)
        print("Seeding Misconfiguration Findings Register")
        print("=" * 70)
        if a.Finding.query.count() == 0:
            rule_lookup = {rid: (title, sev) for rid, title, sev in a.CSPM_RULES}
            for rule_id, resource_name, status, owner, description in FINDINGS:
                title, severity = rule_lookup[rule_id]
                f = a.Finding(
                    rule_id=rule_id, title=title, severity=severity,
                    description=description, resource_id=resource_map[resource_name].id,
                    status=status, owner=owner,
                )
                a.db.session.add(f)
                a.db.session.commit()
                flag = " ⚠ CAPITAL ONE REPLAY" if rule_id == "CSPM-05" else ""
                print(f"  [{severity:8s}] {rule_id} on {resource_name} -> {status}{flag}")
            a.db.session.commit()
        else:
            print("  Findings already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full CSPM demo dataset loaded")

        findings = a.Finding.query.all()
        score = a.posture_score(findings)
        print()
        print("=" * 70)
        print(f"Done. {a.CloudResource.query.count()} resources, {len(findings)} findings seeded.")
        print(f"Current Cloud Security Posture Score: {score}/100")
        print("Visit /dashboard for the overview, or /report for the printable")
        print("audit-ready report.")
        print("=" * 70)


if __name__ == "__main__":
    main()
