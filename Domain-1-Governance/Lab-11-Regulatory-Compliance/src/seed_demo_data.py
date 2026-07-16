"""
Seed demo data for the Regulatory Compliance Tracker (Lab 12).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec regulatory-compliance python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
from datetime import datetime, timedelta

import app as a

now = datetime.utcnow()

FRAMEWORKS = [
    ("SAMA CSF", "SAMA", 2, "All SAMA-regulated activity: banking, payments, credit", "Khalid Al-Mutairi"),
    ("PDPL", "SDAIA", 72, "All personal data of individuals in Saudi Arabia", "Khalid Al-Mutairi"),
    ("NCA ECC", "NCA", 24, "Critical national infrastructure / government-linked systems", "Khalid Al-Mutairi"),
    ("PCI-DSS", "PCI Security Standards Council", 72, "Cardholder data environment (SecurePay platform)", "Fatimah Al-Zahrani"),
    ("SWIFT CSP", "SWIFT", 24, "SWIFT terminal and payment messaging infrastructure", "Noura Al-Qahtani"),
]

# (title, discovered_offset_hours_ago, severity, description, affected_data, framework_names,
#  notified_offset_hours_ago_per_framework or None list, notes)
# We'll build incidents individually below for clarity given the per-framework notification timing complexity.


def get_or_create_framework(name, regulator, hours, scope, owner):
    existing = a.RegulatoryFramework.query.filter_by(name=name).first()
    if existing:
        return existing, False
    fw = a.RegulatoryFramework(name=name, regulator=regulator, critical_notification_deadline_hours=hours,
                                scope_description=scope, owner=owner)
    a.db.session.add(fw)
    a.db.session.commit()
    return fw, True


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding Regulatory Framework Register")
        print("=" * 70)
        fw_map = {}
        for name, regulator, hours, scope, owner in FRAMEWORKS:
            fw, created = get_or_create_framework(name, regulator, hours, scope, owner)
            fw_map[name] = fw
            print(f"  [{'CREATED' if created else 'exists'}] {name} — {hours}h deadline ({regulator})")

        print()
        print("=" * 70)
        print("Seeding Incidents & Notification Requirements")
        print("=" * 70)

        if a.Incident.query.count() == 0:
            # --- Incident 1: THE UBER REPLAY ---
            # Discovered ~400 days ago, notified only ~370 days ago (i.e. ~30 days after discovery is
            # still catastrophically late against 2h/72h deadlines) - but to really replay Uber we push
            # the actual notification even further out: notified only 5 days ago, ~395 days after discovery.
            uber_discovered = now - timedelta(days=400)
            uber_notified = now - timedelta(days=5)
            inc1 = a.Incident(
                title="Historical Payment Data Exposure — Concealed, Not Reported at Time of Discovery",
                discovered_at=uber_discovered, severity="Critical",
                description=(
                    "A third-party service used for backup storage was found to have exposed payment "
                    "transaction records. Rather than notifying SAMA and SDAIA at the time, the incident "
                    "was handled informally and the exposed data set was confirmed deleted by the party who "
                    "accessed it, with no regulatory notification made. This is a direct replay of the "
                    "2016/2017 Uber breach concealment pattern — see docs/case-study-uber-breach.md. The "
                    "incident was only formally logged and reported to regulators after a governance review "
                    "surfaced it, roughly 400 days after the original discovery."
                ),
                affected_data_types="names, partial card numbers, transaction history",
            )
            a.db.session.add(inc1)
            a.db.session.commit()
            for fw_name in ["SAMA CSF", "PDPL", "PCI-DSS"]:
                req = a.NotificationRequirement(
                    incident_id=inc1.id, framework_id=fw_map[fw_name].id,
                    deadline_hours=fw_map[fw_name].critical_notification_deadline_hours,
                    notified_at=uber_notified,
                    notes="Notified only after internal governance review surfaced the historical incident — "
                          "not proactively reported at time of discovery.",
                )
                a.db.session.add(req)
            a.db.session.commit()
            print(f"  [CREATED] {inc1.title[:60]} -> 3 notification requirements, ALL notified ~395 days late")

            # --- Incident 2: Well-handled Critical incident, notified on time across all applicable frameworks ---
            inc2_discovered = now - timedelta(days=20)
            inc2 = a.Incident(
                title="SecurePay Payment Switch Anomalous Access Attempt",
                discovered_at=inc2_discovered, severity="Critical",
                description="Automated monitoring flagged and blocked an anomalous privileged access attempt "
                             "on the Payment Switch Server (see Lab 03 asset inventory). No data was exfiltrated, "
                             "but the attempt met the criteria for mandatory regulatory notification given the "
                             "sensitivity of the system involved.",
                affected_data_types="none confirmed exfiltrated — precautionary notification",
            )
            a.db.session.add(inc2)
            a.db.session.commit()
            for fw_name, notify_offset_hours in [("SAMA CSF", 1.5), ("PCI-DSS", 40)]:
                req = a.NotificationRequirement(
                    incident_id=inc2.id, framework_id=fw_map[fw_name].id,
                    deadline_hours=fw_map[fw_name].critical_notification_deadline_hours,
                    notified_at=inc2_discovered + timedelta(hours=notify_offset_hours),
                    notes="Notified within SLA per the Escalation Matrix (see Lab 04).",
                )
                a.db.session.add(req)
            a.db.session.commit()
            print(f"  [CREATED] {inc2.title[:60]} -> 2 notification requirements, both ON TIME")

            # --- Incident 3: Currently open, within window (demonstrates a live/pending clock) ---
            inc3_discovered = now - timedelta(hours=8)
            inc3 = a.Incident(
                title="Suspicious Third-Party API Integration Traffic Pattern",
                discovered_at=inc3_discovered, severity="High",
                description="Unusual outbound traffic volume detected from the Third-Party Loyalty Program "
                             "Integration (see Lab 08 project register). Under investigation; precautionary "
                             "notification clocks started per policy while root cause is confirmed.",
                affected_data_types="under investigation",
            )
            a.db.session.add(inc3)
            a.db.session.commit()
            for fw_name in ["PDPL", "NCA ECC"]:
                req = a.NotificationRequirement(
                    incident_id=inc3.id, framework_id=fw_map[fw_name].id,
                    deadline_hours=fw_map[fw_name].critical_notification_deadline_hours,
                    notified_at=None,
                )
                a.db.session.add(req)
            a.db.session.commit()
            print(f"  [CREATED] {inc3.title[:60]} -> 2 notification requirements, PENDING (within window)")

            # --- Incident 4: Currently overdue and NOT yet notified (live warning example) ---
            inc4_discovered = now - timedelta(hours=100)
            inc4 = a.Incident(
                title="SWIFT Terminal Configuration Drift Detected",
                discovered_at=inc4_discovered, severity="High",
                description="Internal review found the SWIFT Terminal Workstation (see Lab 03) had drifted from "
                             "its approved security configuration baseline for an unknown period. SWIFT CSP "
                             "notification obligation triggered but not yet completed.",
                affected_data_types="none confirmed — configuration finding",
            )
            a.db.session.add(inc4)
            a.db.session.commit()
            req4 = a.NotificationRequirement(
                incident_id=inc4.id, framework_id=fw_map["SWIFT CSP"].id,
                deadline_hours=fw_map["SWIFT CSP"].critical_notification_deadline_hours,
                notified_at=None,
            )
            a.db.session.add(req4)
            a.db.session.commit()
            print(f"  [CREATED] {inc4.title[:60]} -> 1 notification requirement, currently OVERDUE")
        else:
            print("  Incidents already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Compliance Gap Register")
        print("=" * 70)
        GAPS = [
            ("Cloud Security Policy Gap", "NCA ECC", "High", "Khalid Al-Mutairi", -10, 20, "Open",
             "Cross-referenced from Lab 06 Coverage Gap Analysis and Lab 07 CSPM findings — no active Cloud "
             "Security Policy currently exists.", "Lab 06 / Lab 07"),
            ("Third-Party & M&A Security Integration Policy Still Draft", "SAMA CSF", "Medium",
             "Khalid Al-Mutairi", -10, 45, "Open",
             "Cross-referenced from Lab 06 and Lab 11 — policy has remained in Draft status across multiple "
             "review cycles.", "Lab 06 / Lab 11"),
            ("Build Infrastructure Access Control Weakness", "NCA ECC", "Critical", "Omar Al-Shammari", -690, -660,
             "Open", "Cross-referenced from Lab 11's audit findings register — Critical, repeat finding, "
             "660+ days overdue against its remediation SLA.", "Lab 11"),
            ("Data Localization Confirmation Pending for New Cloud Region", "PDPL", "Medium",
             "Fatimah Al-Zahrani", -15, 30, "In Progress",
             "Confirming all personal data in the newly adopted cloud region remains within approved "
             "data-residency boundaries per PDPL.", None),
            ("PCI-DSS Quarterly ASV Scan Overdue", "PCI-DSS", "High", "Fatimah Al-Zahrani", -5, 10, "Open",
             "Required quarterly Approved Scanning Vendor scan has not been completed on schedule.", None),
            ("SWIFT CSP Self-Attestation Not Yet Submitted", "SWIFT CSP", "Medium", "Noura Al-Qahtani", -20, 15,
             "Verified Closed", "Annual SWIFT CSP self-attestation completed and submitted.", None),
        ]
        if a.ComplianceGap.query.count() == 0:
            for title, fw_name, sev, owner, id_offset, due_offset, status, desc, xref in GAPS:
                g = a.ComplianceGap(
                    framework_id=fw_map[fw_name].id, title=title, description=desc, severity=sev, owner=owner,
                    identified_at=(now + timedelta(days=id_offset)).strftime("%Y-%m-%d"),
                    due_date=(now + timedelta(days=due_offset)).strftime("%Y-%m-%d"),
                    status=status, cross_reference=xref,
                )
                a.db.session.add(g)
                flag = " ⚠ CROSS-REFERENCED FROM EARLIER LAB" if xref else ""
                print(f"  [{sev:8s}] {title}{flag}")
            a.db.session.commit()
        else:
            print("  Gaps already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Regulatory Correspondence Log")
        print("=" * 70)
        CORRESPONDENCE = [
            ("SAMA CSF", "SAMA", "Examination Request", -30, "SAMA CSF annual compliance examination — document request", "Responded", -10, None),
            ("SAMA CSF", "SAMA", "Formal Inquiry", -8, "Follow-up inquiry regarding the historical payment data exposure incident", "Open", 2, "Response due imminently — see the Uber-replay incident in Notification Tracker"),
            ("PDPL", "SDAIA", "Breach Notification", -5, "Formal breach notification submission for the historical payment data exposure incident", "Responded", -3, None),
            ("PCI-DSS", "PCI Security Standards Council", "Routine Filing", -60, "Annual Report on Compliance (ROC) submission", "Closed", -55, None),
            ("SWIFT CSP", "SWIFT", "Formal Inquiry", -3, "Inquiry regarding SWIFT Terminal configuration drift finding", "Open", 5, None),
        ]
        if a.RegulatoryCorrespondence.query.count() == 0:
            for fw_name, regulator, ctype, date_offset, subject, status, due_offset, notes in CORRESPONDENCE:
                c = a.RegulatoryCorrespondence(
                    framework_id=fw_map[fw_name].id, regulator=regulator, correspondence_type=ctype,
                    date=(now + timedelta(days=date_offset)).strftime("%Y-%m-%d"), subject=subject, status=status,
                    due_date=(now + timedelta(days=due_offset)).strftime("%Y-%m-%d"), notes=notes,
                )
                a.db.session.add(c)
                print(f"  [{status:10s}] {subject[:55]}")
            a.db.session.commit()
        else:
            print("  Correspondence already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full Regulatory Compliance demo dataset loaded")

        all_reqs = a.NotificationRequirement.query.all()
        rate = a.on_time_rate(all_reqs)
        print()
        print("=" * 70)
        print(f"Done. {a.RegulatoryFramework.query.count()} frameworks, {a.Incident.query.count()} incidents, "
              f"{len(all_reqs)} notification requirements seeded.")
        print(f"Current on-time notification rate: {rate}%")
        print("Visit /dashboard for the overview, or /report for the printable")
        print("audit-ready report.")
        print("=" * 70)


if __name__ == "__main__":
    main()
