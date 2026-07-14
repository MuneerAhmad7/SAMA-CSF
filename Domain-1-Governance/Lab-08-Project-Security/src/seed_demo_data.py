"""
Seed demo data for the Project Security Gate Tracker (Lab 08).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec project-security python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
import app as a

PROJECTS = [
    ("Payment Checkout Redesign", "Feature Enhancement", "Payments", "Critical", "Yousef Al-Harbi"),
    ("Mobile Banking App v3.0", "New Application", "Digital Channels", "Critical", "Layla Al-Ghamdi"),
    ("Third-Party Loyalty Program Integration", "Third-Party Integration", "Marketing", "Medium", "Sara Al-Dosari"),
    ("Core Banking DB Migration", "Infrastructure Change", "IT Operations", "Critical", "Fatimah Al-Zahrani"),
    ("Internal HR Portal Refresh", "Feature Enhancement", "Human Resources", "Low", "Noura Al-Qahtani"),
    ("Customer Support Chatbot", "New Application", "Customer Experience", "Medium", "Omar Al-Shammari"),
]

# gate statuses per project, in GATE_NAMES order: Initiation, Design, Build, Test, Deploy, Post-Implementation
GATE_DATA = {
    "Payment Checkout Redesign": [
        ("Passed", "Khalid Al-Mutairi", "2026-01-10", "Security requirements documented, threat model reviewed"),
        ("Passed", "Khalid Al-Mutairi", "2026-01-25", "Design reviewed, PCI-DSS scope confirmed"),
        ("Passed", "Fatimah Al-Zahrani", "2026-02-15", "Code review completed, secure coding checklist followed"),
        ("Passed", "Fatimah Al-Zahrani", "2026-03-01", "SAST/DAST completed, no critical findings"),
        ("Waived", "Yousef Al-Harbi", "2026-03-10",
         "⚠ DEPLOY GATE WAIVED under release deadline pressure — a follow-up hotfix script was pushed to the "
         "live payment page without a formal security sign-off. This is the exact failure mode behind the "
         "2018 British Airways breach. See docs/case-study-british-airways-breach.md."),
        ("Not Started", None, None, None),
    ],
    "Mobile Banking App v3.0": [
        ("Passed", "Khalid Al-Mutairi", "2025-11-01", ""),
        ("Passed", "Khalid Al-Mutairi", "2025-11-20", ""),
        ("Passed", "Layla Al-Ghamdi", "2026-01-05", ""),
        ("Passed", "Fatimah Al-Zahrani", "2026-01-28", "Pentest completed, findings remediated (see Lab 03)"),
        ("Passed", "Khalid Al-Mutairi", "2026-02-05", "Full sign-off obtained before App Store submission"),
        ("In Progress", "Layla Al-Ghamdi", None, "30-day post-launch review scheduled"),
    ],
    "Third-Party Loyalty Program Integration": [
        ("Passed", "Khalid Al-Mutairi", "2026-02-01", ""),
        ("Passed", "Khalid Al-Mutairi", "2026-02-10", "Data sharing agreement reviewed by Legal"),
        ("In Progress", "Sara Al-Dosari", None, "Vendor API integration code under review"),
        ("Not Started", None, None, None),
        ("Not Started", None, None, None),
        ("Not Started", None, None, None),
    ],
    "Core Banking DB Migration": [
        ("Passed", "Khalid Al-Mutairi", "2025-09-01", ""),
        ("Passed", "Fatimah Al-Zahrani", "2025-09-20", "Encryption and access control design reviewed"),
        ("Passed", "Fatimah Al-Zahrani", "2025-11-01", ""),
        ("Passed", "Fatimah Al-Zahrani", "2025-12-01", "Migration tested in staging with production-like data volume"),
        ("Passed", "Khalid Al-Mutairi", "2025-12-15", ""),
        ("Passed", "Fatimah Al-Zahrani", "2026-01-15", "Post-migration review completed, no issues found"),
    ],
    "Internal HR Portal Refresh": [
        ("Passed", "Khalid Al-Mutairi", "2026-03-01", ""),
        ("In Progress", "Noura Al-Qahtani", None, ""),
        ("Not Started", None, None, None),
        ("Not Started", None, None, None),
        ("Not Started", None, None, None),
        ("Not Started", None, None, None),
    ],
    "Customer Support Chatbot": [
        ("Passed", "Khalid Al-Mutairi", "2026-02-20", ""),
        ("Passed", "Khalid Al-Mutairi", "2026-03-01", ""),
        ("Failed", "Omar Al-Shammari", "2026-03-15",
         "Code review found the chatbot logging full conversation transcripts, including any accidentally "
         "pasted card numbers, without redaction. Sent back for remediation."),
        ("Not Started", None, None, None),
        ("Not Started", None, None, None),
        ("Not Started", None, None, None),
    ],
}

SCRIPTS = [
    ("payment-widget.js", "Payment Checkout Page", "https://cdn.falakpay.example/payment-widget.js", True, "2026-01-20", "Critical", "Core payment form handler, SRI pinned and reviewed."),
    ("analytics-tracker.js", "Payment Checkout Page", "https://cdn.thirdparty-analytics.example/tracker.js", False, "2025-08-01",
     "Critical",
     "⚠ NO SRI HASH PINNED — third-party analytics script running on the payment page has not been "
     "integrity-verified since initial integration 7+ months ago. This is the exact gap that allowed the "
     "malicious Magecart script to run undetected on British Airways' payment page in 2018."),
    ("chat-widget.js", "Customer Support Page", "https://cdn.falakpay.example/chat-widget.js", True, "2026-02-10", "Low", "Support chat widget, low risk, SRI pinned."),
    ("loyalty-partner-sdk.js", "Loyalty Program Page", "https://sdk.loyaltypartner.example/sdk.js", False, "2025-12-01", "Medium", "Third-party loyalty SDK, SRI pinning planned as part of integration hardening."),
    ("session-recorder.js", "Mobile Banking Login Page", "https://cdn.falakpay.example/session-recorder.js", True, "2026-02-01", "High", "Session replay tool for UX research, SRI pinned after security review flagged the risk."),
    ("marketing-pixel.js", "Corporate Website Homepage", "https://pixel.marketingvendor.example/px.js", False, "2025-06-01", "Low", "Low-risk marketing pixel on non-transactional page."),
    ("core-banking-widget.js", "Core Banking Dashboard", "https://cdn.falakpay.example/core-banking-widget.js", True, "2026-01-05", "Critical", "Internal dashboard widget, SRI pinned, reviewed quarterly."),
    ("hr-portal-forms.js", "Internal HR Portal", "https://cdn.falakpay.example/hr-forms.js", False, "2025-10-01", "Low", "Internal-only, low external exposure risk."),
]

# (title, project_name, change_type, deployed_at, gate_passed, approver, notes)
CHANGES = [
    ("Payment page hotfix — analytics script update", "Payment Checkout Redesign", "Code deploy", "2026-03-12", False,
     "Yousef Al-Harbi",
     "⚠ Deployed directly to the live payment page to fix a tracking bug, without going back through the "
     "Deploy gate (which had been Waived, not Passed). No formal security sign-off obtained for this specific change."),
    ("Mobile app v3.0 production release", "Mobile Banking App v3.0", "App release", "2026-02-06", True,
     "Khalid Al-Mutairi", "Deployed after full Deploy gate sign-off."),
    ("Core banking DB cutover", "Core Banking DB Migration", "Infrastructure change", "2025-12-16", True,
     "Khalid Al-Mutairi", "Executed per approved migration runbook."),
    ("Emergency config change — increase API rate limit", None, "Config change", "2026-03-05", True,
     "Omar Al-Shammari", "Approved emergency change, documented and reviewed within 24 hours per exception process."),
]


def get_or_create_project(name, ptype, bu, criticality, owner):
    existing = a.Project.query.filter_by(name=name).first()
    if existing:
        return existing, False
    p = a.Project(name=name, project_type=ptype, business_unit=bu, criticality=criticality, owner=owner)
    a.db.session.add(p)
    a.db.session.commit()
    for gate_name in a.GATE_NAMES:
        a.db.session.add(a.SecurityGate(project_id=p.id, gate_name=gate_name, status="Not Started"))
    a.db.session.commit()
    return p, True


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding Project Register for Falak Pay Financial Company")
        print("=" * 70)
        project_map = {}
        for name, ptype, bu, crit, owner in PROJECTS:
            p, created = get_or_create_project(name, ptype, bu, crit, owner)
            project_map[name] = p
            print(f"  [{'CREATED' if created else 'exists'}] {name} ({crit})")

        print()
        print("=" * 70)
        print("Scoring Security Gates")
        print("=" * 70)
        for project_name, gate_list in GATE_DATA.items():
            project = project_map[project_name]
            gates = sorted(project.gates, key=lambda g: a.GATE_NAMES.index(g.gate_name))
            for gate, (status, approver, gate_date, notes) in zip(gates, gate_list):
                gate.status = status
                gate.approver = approver
                gate.gate_date = gate_date
                gate.evidence_notes = notes
            print(f"  {project_name}: {[g[0] for g in gate_list]}")
        a.db.session.commit()

        print()
        print("=" * 70)
        print("Seeding Third-Party Script / Code Integrity Register")
        print("=" * 70)
        if a.ThirdPartyScript.query.count() == 0:
            for name, page, url, sri, reviewed, risk, notes in SCRIPTS:
                a.db.session.add(a.ThirdPartyScript(
                    name=name, page_context=page, source_url=url, sri_pinned=sri,
                    last_reviewed=reviewed, risk_level=risk, notes=notes,
                ))
                flag = " ⚠ BA MAGECART REPLAY (no SRI, high risk page)" if not sri and risk in ("Critical", "High") else ""
                print(f"  [{'SRI OK' if sri else 'NO SRI':7s}] {name} on {page}{flag}")
            a.db.session.commit()
        else:
            print("  Scripts already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Change Log")
        print("=" * 70)
        if a.ChangeRecord.query.count() == 0:
            for title, project_name, ctype, deployed, gate_passed, approver, notes in CHANGES:
                pid = project_map[project_name].id if project_name else None
                a.db.session.add(a.ChangeRecord(
                    project_id=pid, title=title, change_type=ctype, deployed_at=deployed,
                    gate_passed=gate_passed, approver=approver, notes=notes,
                ))
                flag = " ⚠ UNGATED CHANGE" if not gate_passed else ""
                print(f"  [{'GATED' if gate_passed else 'UNGATED':8s}] {title}{flag}")
            a.db.session.commit()
        else:
            print("  Changes already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full Project Security demo dataset loaded")

        print()
        print("=" * 70)
        print("Done. Visit /dashboard for the overview, or /report for the")
        print("printable audit-ready report.")
        print("=" * 70)


if __name__ == "__main__":
    main()
