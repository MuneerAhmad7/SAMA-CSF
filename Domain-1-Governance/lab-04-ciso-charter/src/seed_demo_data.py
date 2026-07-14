"""
Seed demo data for the CISO Charter Builder (Lab 04).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec ciso-charter python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
import app as a

CHARTER_DATA = {
    "organization_name": "Falak Pay Financial Company",
    "ciso_name": "Khalid Al-Mutairi",
    "reports_to": "CEO, with a direct dotted line to the Board Risk & Compliance Committee",
    "mandate_statement": (
        "The CISO holds full authority to define, implement, and enforce the organization's "
        "cybersecurity strategy and controls across all business units, systems, and third parties, "
        "independent of IT operational priorities. This mandate was formalized following an internal "
        "governance review that specifically referenced the 2013 Target breach as a cautionary case "
        "of what happens without a Charter like this one."
    ),
    "independence_statement": (
        "The Cybersecurity function is a standalone department reporting to the CEO, organizationally "
        "separate from the IT department (which reports to the CTO). The CISO does not report through, "
        "or require sign-off from, IT leadership for security decisions."
    ),
    "budget_authority": "CISO may approve security spend independently up to SAR 500,000 per initiative without further Board approval.",
    "escalation_authority": (
        "The CISO may escalate any Critical or High security event directly to the CEO and Board Risk "
        "Committee Chair at any time, without requiring IT Director or CTO approval or notification first. "
        "This right is explicit in this Charter specifically because its absence was a key structural gap "
        "identified in the Target 2013 breach."
    ),
    "committee_name": "Falak Pay Cyber Security Committee",
    "committee_frequency": "Quarterly minimum (monthly during the first 12 months of this Charter)",
    "term_review_cycle": "Annual, or immediately following any Critical security incident",
    "board_reporting_frequency": "Quarterly, with immediate ad-hoc reporting for Critical incidents",
    "scope_statement": (
        "This Charter's authority covers all Falak Pay business units, all IT and OT systems, all "
        "customer-facing and internal applications, and all third-party/vendor relationships with "
        "access to Falak Pay systems or data, including payment processing infrastructure (SecurePay)."
    ),
}

AUTHORITY_STATUS = {
    "AUTH-1": ("Implemented", "Org chart shows Cybersecurity as standalone function reporting to CEO, separate from IT/CTO line"),
    "AUTH-2": ("Implemented", "Charter Section 1, approved by Board 15 March 2026"),
    "AUTH-3": ("Implemented", "Charter Section 6 — direct escalation right explicitly documented"),
    "AUTH-4": ("Implemented", "Charter Section 5 — SAR 500,000 independent approval threshold"),
    "AUTH-5": ("Implemented", "Charter Section 3 — scope covers all business units"),
    "AUTH-6": ("Implemented", "CISO chairs the Falak Pay Cyber Security Committee"),
    "AUTH-7": ("Partial", "Incident severity classification exists in Incident Response Plan, but 'critical' declaration authority not yet cross-referenced in this Charter — action item for next review"),
    "AUTH-8": ("Implemented", "See Escalation Matrix module — SOC alerts routed per documented SLA"),
    "AUTH-9": ("Implemented", "CISO KPIs set by CEO and Board Committee, independent of CTO input"),
    "AUTH-10": ("Partial", "Informal practice exists; formal override/appeal process not yet documented — recommend adding in next Charter revision"),
    "AUTH-11": ("Implemented", "Board Risk & Compliance Committee approval on file, 15 March 2026"),
    "AUTH-12": ("Implemented", "Annual review cycle documented in Charter Section 8"),
    "AUTH-13": ("Partial", "Third-party risk policy references CISO sign-off for Critical vendors; threshold value not yet formally set"),
    "AUTH-14": ("Not Implemented", "No documented succession/continuity plan for the CISO role yet — flagged as a gap for next Committee meeting"),
}

RACI_ENTRIES = [
    ("Approve/amend CISO Charter", "CISO", "Board Risk & Compliance Committee", "Legal, CEO", "All Staff"),
    ("Declare a Critical security incident", "SOC Lead", "CISO", "CEO", "Board Risk Committee"),
    ("Approve security budget > SAR 500,000", "CISO", "Board Risk & Compliance Committee", "CFO", "—"),
    ("Halt a project on security grounds", "CISO", "CISO", "Project Owner, CTO", "Board Risk Committee"),
    ("Approve third-party/vendor security exceptions", "CISO", "CISO", "Legal, Procurement", "Board Risk Committee"),
    ("Set CISO performance objectives", "CEO", "Board Risk & Compliance Committee", "CISO", "—"),
    ("Report quarterly security posture to Board", "CISO", "Board Risk & Compliance Committee", "—", "All Staff"),
    ("Review/update Escalation Matrix", "CISO", "CISO", "SOC Lead, Legal", "Board Risk Committee"),
]

ESCALATION_RULES = [
    ("Critical", "Confirmed data exfiltration or active ransomware", "CISO + CEO + Board Risk Committee Chair", "Immediate (within 30 min)"),
    ("Critical", "Regulatory-reportable breach (SAMA/PDPL threshold met)", "CISO + CEO + Legal + SDAIA/SAMA notification", "Within 2 hours (SAMA) / 72 hours (PDPL)"),
    ("High", "Malware detected on payment-critical system", "CISO + Head of Payments Ops", "Within 1 hour"),
    ("High", "SOC alert with no automatic containment triggered", "CISO + SOC Lead", "Within 4 hours"),
    ("Medium", "Repeated failed privileged login attempts", "SOC Lead + IAM Owner", "Within 24 hours"),
    ("Low", "Routine vulnerability scan finding", "Vulnerability Management Owner", "Per patch SLA (see Lab 03)"),
]


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding CISO Charter for Falak Pay Financial Company (fictional)")
        print("=" * 70)
        for key, value in CHARTER_DATA.items():
            field = a.CharterField.query.filter_by(field_key=key).first()
            if field:
                print(f"  [exists] {key}")
                continue
            a.db.session.add(a.CharterField(field_key=key, value=value))
            print(f"  [SET] {key}")
        a.db.session.commit()

        print()
        print("=" * 70)
        print("Scoring Authority & Independence Assessment")
        print("=" * 70)
        for control_id, (status, evidence) in AUTHORITY_STATUS.items():
            c = a.AuthorityControl.query.filter_by(control_id=control_id).first()
            if c:
                c.status = status
                c.evidence = evidence
                print(f"  [{status:15s}] {control_id}")
        a.db.session.commit()

        print()
        print("=" * 70)
        print("Seeding RACI matrix")
        print("=" * 70)
        if a.RaciEntry.query.count() == 0:
            for activity, r, acc, c, i in RACI_ENTRIES:
                a.db.session.add(a.RaciEntry(activity=activity, responsible=r, accountable=acc, consulted=c, informed=i))
                print(f"  [ADDED] {activity}")
            a.db.session.commit()
        else:
            print("  RACI already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Escalation Matrix")
        print("=" * 70)
        if a.EscalationRule.query.count() == 0:
            for severity, trigger, escalate_to, timeframe in ESCALATION_RULES:
                a.db.session.add(a.EscalationRule(severity=severity, trigger=trigger, escalate_to=escalate_to, timeframe=timeframe))
                print(f"  [{severity:8s}] {trigger}")
            a.db.session.commit()
        else:
            print("  Escalation rules already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full CISO Charter demo dataset loaded")

        print()
        print("=" * 70)
        print("Done. Visit /dashboard for the maturity overview, or /report for the")
        print("full board-ready Charter document (printable to PDF).")
        print("=" * 70)


if __name__ == "__main__":
    main()
