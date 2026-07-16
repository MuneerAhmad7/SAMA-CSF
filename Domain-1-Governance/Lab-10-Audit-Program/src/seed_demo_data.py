"""
Seed demo data for the Cyber Security Audit & Assurance Tracker (Lab 11).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec audit-assurance python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
from datetime import datetime, timedelta

import app as a

now = datetime.utcnow()


def d(days_offset):
    return (now + timedelta(days=days_offset)).strftime("%Y-%m-%d")


ENGAGEMENTS = [
    ("FY2025 Internal Cybersecurity Audit", "Internal Audit", "Enterprise-wide control review", -400, -350, "Internal Audit Team", "Report Issued"),
    ("FY2024 Internal Security Review — Build & Release Infrastructure", "Internal Audit",
     "CI/CD pipeline and release infrastructure access controls", -720, -690, "Internal Audit Team", "Report Issued"),
    ("External ISO 27001 Surveillance Audit", "External Audit", "ISMS scope, all domains", -180, -160, "Al-Rashid & Co. Certification Body", "Report Issued"),
    ("Annual Penetration Test — Payment Systems", "Penetration Test", "SecurePay platform, core banking perimeter", -60, -45, "Independent Security Assessor", "Report Issued"),
    ("SAMA Regulatory Examination", "Regulatory Examination", "SAMA CSF compliance, all domains", -30, -10, "SAMA Examination Team", "Completed"),
]

# (title, category, engagement_name, severity, status_days_ago_identified, status, owner, is_repeat, repeat_notes, description, recommendation, root_cause)
FINDINGS = [
    # --- THE SOLARWINDS REPLAY: Critical, build infrastructure, identified early, still overdue, flagged as repeat ---
    ("Weak Access Controls on Build & Release Infrastructure", "Build Pipeline Security",
     "FY2024 Internal Security Review — Build & Release Infrastructure", "Critical", 690, "Open",
     "Omar Al-Shammari", False, None,
     "Shared service account with a weak, infrequently-rotated password used for deployment access to the "
     "build pipeline, with no MFA enforced. Identified during the FY2024 internal review.",
     "Implement individual, MFA-protected accounts for all build/release infrastructure access; eliminate "
     "shared service account credentials.",
     "This finding was never fully remediated after the FY2024 review — see FY2025 audit below where it "
     "resurfaces as a repeat finding. This is a direct replay of the governance failure pattern behind the "
     "2020 SolarWinds breach: a known build-infrastructure weakness that sat unremediated. "
     "See docs/case-study-solarwinds-breach.md."),

    ("Weak Access Controls on Build & Release Infrastructure (Repeat)", "Build Pipeline Security",
     "FY2025 Internal Cybersecurity Audit", "Critical", 350, "Open", "Omar Al-Shammari", True,
     "Originally identified in the FY2024 Internal Security Review — Build & Release Infrastructure engagement, "
     "over 300 days prior. Remediation was never completed or verified.",
     "Same underlying weakness identified again in the FY2025 audit — the shared, weakly-protected build "
     "service account is still in use, now over a year since first identified.",
     "Escalate to CISO immediately; treat as a Critical, board-visible risk given the potential blast radius "
     "of a compromised build pipeline (see SolarWinds case).",
     "Repeat finding — same root cause as the FY2024 finding, not yet addressed."),

    # --- FY2025 Internal Audit — other findings ---
    ("Privileged Access Review Not Performed Quarterly as Required", "Access Management",
     "FY2025 Internal Cybersecurity Audit", "High", 350, "Verified Closed", "Noura Al-Qahtani", False, None,
     "Quarterly privileged access reviews (required per Lab 01's governance tracker policy) had lapsed for "
     "two consecutive quarters.", "Reinstate quarterly review cadence with calendar reminders and named owner.",
     "Process was documented but not calendared/owned after a personnel change."),

    ("Data Retention Policy Not Consistently Applied", "Data Protection",
     "FY2025 Internal Cybersecurity Audit", "Medium", 350, "Remediated", "Fatimah Al-Zahrani", False, None,
     "Sample testing found some legacy customer records retained beyond the policy-defined retention period.",
     "Implement automated retention enforcement rather than manual review.",
     "Manual retention process was error-prone at scale."),

    ("Physical Access Logs Not Reviewed Monthly", "Physical Security",
     "FY2025 Internal Cybersecurity Audit", "Low", 350, "Verified Closed", "Omar Al-Shammari", False, None,
     "Physical access logs for the data center were collected but not formally reviewed on the required monthly cadence.",
     "Assign monthly review to a named owner with sign-off tracking.", "No formal ownership assigned."),

    # --- External ISO 27001 Audit findings ---
    ("Risk Register Not Updated Following Organizational Changes", "Risk Management",
     "External ISO 27001 Surveillance Audit", "Medium", 160, "Verified Closed", "Fatimah Al-Zahrani", False, None,
     "Risk register referenced an outdated organizational structure following a department reorganization.",
     "Tie risk register review to the HR change-management process.", "No trigger existed linking org changes to risk register updates."),

    ("Supplier Security Assessments Overdue for 2 Vendors", "Third-Party Risk",
     "External ISO 27001 Surveillance Audit", "Medium", 160, "In Progress", "Khalid Al-Mutairi", False, None,
     "Annual security reassessment overdue for 2 of Falak Pay's critical third-party vendors.",
     "Complete overdue reassessments and implement automated reminders ahead of the annual deadline.",
     "Vendor reassessment tracking was manual and slipped during a busy period."),

    # --- Pentest findings ---
    ("SQL Injection in Legacy Reporting Module", "Application Security",
     "Annual Penetration Test — Payment Systems", "High", 45, "Remediated", "Layla Al-Ghamdi", False, None,
     "Legacy internal reporting module vulnerable to SQL injection via an unsanitized filter parameter.",
     "Patch applied and parameterized queries implemented; retested and confirmed fixed.",
     "Module predated current secure coding standards (see Lab 08) and was not in regular SAST scope."),

    ("Session Tokens Not Invalidated on Password Change", "Application Security",
     "Annual Penetration Test — Payment Systems", "Medium", 45, "Open", "Layla Al-Ghamdi", False, None,
     "Active sessions remain valid after a user changes their password, rather than being force-invalidated.",
     "Implement session invalidation on password change across all authenticated services.",
     "Not part of the original authentication design; identified during penetration testing."),

    ("Verbose Error Messages Reveal Stack Traces", "Application Security",
     "Annual Penetration Test — Payment Systems", "Low", 45, "Verified Closed", "Layla Al-Ghamdi", False, None,
     "Some error pages revealed internal stack traces to end users.",
     "Deploy custom error pages across all environments.", "Default framework error handling was left enabled."),

    # --- SAMA Regulatory Examination findings ---
    ("Incident Reporting Timeline Not Consistently Met", "Incident Response",
     "SAMA Regulatory Examination", "High", 10, "Open", "Khalid Al-Mutairi", False, None,
     "Sample testing of incident records found 2 of 8 sampled incidents were reported to SAMA outside the "
     "required 2-hour window for critical incidents.",
     "Automate incident severity classification and SAMA notification triggers to remove manual delay.",
     "Manual escalation process introduced delay during high-activity periods; see Lab 04's Escalation Matrix "
     "for the related governance control."),

    ("Third-Party & M&A Security Integration Policy Still in Draft", "Governance",
     "SAMA Regulatory Examination", "Medium", 10, "Open", "Khalid Al-Mutairi", True,
     "Related to the ongoing gap tracked in Lab 06's Policy Framework — this policy has been in Draft status "
     "across multiple review cycles without reaching Approved status.",
     "Falak Pay's Third-Party & M&A Security Integration Policy has not progressed past Draft status despite "
     "being flagged in a prior internal review.",
     "Finalize and obtain Board approval for this policy given the active under-integrated acquisition already "
     "identified in Lab 06.",
     "Cross-referenced governance gap — see Lab 06 Policy Framework for full context."),

    ("Cloud Security Policy Gap Confirmed", "Cloud Security",
     "SAMA Regulatory Examination", "High", 10, "Open", "Fatimah Al-Zahrani", True,
     "Consistent with the gap identified in Lab 06's Coverage Gap Analysis — no active Cloud Security Policy "
     "exists.",
     "Examiners confirmed no governing Cloud Security Policy is currently in force, consistent with the "
     "internal Coverage Gap Analysis finding.",
     "Draft and approve a Cloud Security Policy as a matter of priority.",
     "Cross-referenced governance gap — see Lab 06 and Lab 07 for full context."),

    ("Annual Penetration Test Scope Did Not Include OT/Cloud Environments", "Audit Scope",
     "SAMA Regulatory Examination", "Medium", 10, "Open", "Khalid Al-Mutairi", False, None,
     "Examiners noted the annual penetration test scope has not yet been extended to cloud infrastructure "
     "(see Lab 07) despite its growing footprint.",
     "Expand next penetration test scope to explicitly include cloud infrastructure and CSPM-tracked assets.",
     "Pentest scope was defined before the cloud footprint's current scale."),
]


def get_or_create_engagement(name, etype, scope, start_offset, end_offset, auditor, status):
    existing = a.AuditEngagement.query.filter_by(name=name).first()
    if existing:
        return existing, False
    e = a.AuditEngagement(name=name, engagement_type=etype, scope=scope,
                           start_date=d(start_offset), end_date=d(end_offset), auditor=auditor, status=status)
    a.db.session.add(e)
    a.db.session.commit()
    return e, True


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding Audit Engagement Register for Falak Pay Financial Company")
        print("=" * 70)
        engagement_map = {}
        for name, etype, scope, start, end, auditor, status in ENGAGEMENTS:
            e, created = get_or_create_engagement(name, etype, scope, start, end, auditor, status)
            engagement_map[name] = e
            print(f"  [{'CREATED' if created else 'exists'}] {name} ({etype})")

        print()
        print("=" * 70)
        print("Seeding Findings Register")
        print("=" * 70)
        if a.Finding.query.count() == 0:
            for (title, category, eng_name, severity, days_ago, status, owner, is_repeat,
                 repeat_notes, description, recommendation, root_cause) in FINDINGS:
                identified_at = now - timedelta(days=days_ago)
                f = a.Finding(
                    engagement_id=engagement_map[eng_name].id, title=title, category=category,
                    severity=severity, description=description, recommendation=recommendation,
                    owner=owner, identified_at=identified_at, status=status, root_cause=root_cause,
                    is_repeat=is_repeat, repeat_notes=repeat_notes,
                )
                if status in a.sla.CLOSED_STATUSES:
                    f.closed_at = identified_at + timedelta(days=max(5, days_ago // 4))
                a.db.session.add(f)
                a.db.session.commit()
                flag = " ⚠ REPEAT FINDING" if is_repeat else ""
                flag2 = " ⚠ SOLARWINDS PATTERN" if "SolarWinds" in (root_cause or "") else ""
                print(f"  [{severity:8s}] {title[:55]:55s} -> {status}{flag}{flag2}")
            a.db.session.commit()
        else:
            print("  Findings already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Committee Reports")
        print("=" * 70)
        if a.CommitteeReport.query.count() == 0:
            reports = [
                (d(-340), "Board Risk & Compliance Committee",
                 "Reviewed FY2025 Internal Cybersecurity Audit results; 12 findings identified across all domains.",
                 "Flagged the Critical build-infrastructure finding as requiring immediate escalation given its "
                 "repeat status from the FY2024 review."),
                (d(-150), "Board Risk & Compliance Committee",
                 "Reviewed External ISO 27001 Surveillance Audit results.",
                 "No Critical findings from this engagement; 2 Medium findings tracked to closure."),
                (d(-5), "Board Risk & Compliance Committee",
                 "Reviewed SAMA Regulatory Examination preliminary results.",
                 "Highlighted the still-open Critical build-infrastructure finding (now 690+ days old) and the "
                 "governance gaps cross-referenced from Lab 06 (Cloud Security Policy, Third-Party & M&A "
                 "Security Integration Policy) as top priorities for the next quarter."),
            ]
            for meeting_date, attendees, summary, overdue in reports:
                a.db.session.add(a.CommitteeReport(
                    meeting_date=meeting_date, attendees=attendees, summary=summary, overdue_highlighted=overdue,
                ))
            a.db.session.commit()
            print(f"  {len(reports)} committee reports logged.")
        else:
            print("  Committee reports already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full Audit & Assurance demo dataset loaded")

        findings = a.Finding.query.all()
        overdue_count = len([f for f in findings if a.sla.is_overdue(f, now)])
        print()
        print("=" * 70)
        print(f"Done. {a.AuditEngagement.query.count()} engagements, {len(findings)} findings seeded.")
        print(f"Overdue findings: {overdue_count}")
        print("Visit /dashboard for the overview, or /report for the printable")
        print("board-ready report.")
        print("=" * 70)


if __name__ == "__main__":
    main()
