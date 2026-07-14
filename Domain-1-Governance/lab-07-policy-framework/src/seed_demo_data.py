"""
Seed demo data for the Policy Framework Manager (Lab 06).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec policy-framework python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
from datetime import datetime, timedelta

import app as a

today = datetime.now()


def d(days_offset):
    return (today + timedelta(days=days_offset)).strftime("%Y-%m-%d")


# (title, type, domain, owner, status, version, effective_offset, review_offset, parent_title, notes)
POLICIES = [
    ("Falak Pay Enterprise Cybersecurity Policy", "Master Policy", "Governance", "Khalid Al-Mutairi",
     "Published", "2.0", -200, 165, None, "Board-approved master policy, see Lab 01"),

    ("Access Control Policy", "Domain Policy", "Identity & Access Management", "Noura Al-Qahtani",
     "Published", "1.3", -180, 185, "Falak Pay Enterprise Cybersecurity Policy", "Covers MFA, PAM, maker-checker (see Lab 02)"),
    ("Privileged Access Management Standard", "Standard", "Identity & Access Management", "Noura Al-Qahtani",
     "Published", "1.1", -150, 215, "Access Control Policy", "PAM tooling requirements"),
    ("User Access Review Procedure", "Procedure", "Identity & Access Management", "Sara Al-Dosari",
     "Published", "1.0", -120, 245, "Access Control Policy", "Quarterly privileged access review steps"),

    ("Data Classification & Protection Policy", "Domain Policy", "Data Protection", "Fatimah Al-Zahrani",
     "Published", "1.4", -160, -15, "Falak Pay Enterprise Cybersecurity Policy",
     "OVERDUE FOR REVIEW — deliberately seeded to demonstrate the SLA alert"),
    ("Data Retention & Disposal Standard", "Standard", "Data Protection", "Fatimah Al-Zahrani",
     "Published", "1.0", -100, 265, "Data Classification & Protection Policy", "NIST SP 800-88 aligned"),

    ("Cryptography & Key Management Policy", "Domain Policy", "Cryptography", "Fatimah Al-Zahrani",
     "Published", "1.2", -140, 225, "Falak Pay Enterprise Cybersecurity Policy", "AES-256, TLS 1.2+, HSM requirements"),

    ("Incident Response Policy", "Domain Policy", "Incident Response", "Khalid Al-Mutairi",
     "Published", "1.5", -170, 195, "Falak Pay Enterprise Cybersecurity Policy", "See Lab 02 incident postmortem template"),
    ("Incident Escalation Procedure", "Procedure", "Incident Response", "Khalid Al-Mutairi",
     "Published", "1.2", -90, 275, "Incident Response Policy", "Cross-references Lab 04 Escalation Matrix"),

    ("Business Continuity & Disaster Recovery Policy", "Domain Policy", "Business Continuity", "Omar Al-Shammari",
     "Approved", "1.0", -30, 335, "Falak Pay Enterprise Cybersecurity Policy", "Pending publication after final Board sign-off"),

    ("Third-Party & M&A Security Integration Policy", "Domain Policy", "Third-Party & M&A Security", "Khalid Al-Mutairi",
     "Draft", "0.3", None, None, "Falak Pay Enterprise Cybersecurity Policy",
     "IN DRAFT — this is the exact policy type that was missing/delayed in the Marriott/Starwood case. "
     "Falak Pay is writing this proactively rather than reactively."),

    ("HR Security Policy (Background Checks, Onboarding/Offboarding)", "Domain Policy", "Human Resources Security",
     "Layla Al-Ghamdi", "Published", "1.1", -110, 255, "Falak Pay Enterprise Cybersecurity Policy", ""),

    ("Physical Security Standard", "Standard", "Physical Security", "Omar Al-Shammari",
     "Review", "1.0", None, None, "Falak Pay Enterprise Cybersecurity Policy", "Under review following office relocation"),

    ("Security Awareness & Training Policy", "Domain Policy", "Security Awareness & Training", "Layla Al-Ghamdi",
     "Published", "1.3", -130, 235, "Falak Pay Enterprise Cybersecurity Policy", "Annual training, quarterly phishing sims"),

    # Note: intentionally NO policy at all for "Cloud Security" domain — a live gap for the Coverage module to catch
]

ENTITIES = [
    ("Falak Pay Digital Wallet Subsidiary", "Wholly-Owned Subsidiary", -900, 95,
     "Minor gap: latest Access Control Policy v1.3 not yet rolled out to subsidiary's legacy admin panel."),
    ("Najm Instant Transfer (acquired Jan 2026)", "Recent Acquisition", -160, 42,
     "SIGNIFICANT GAP — mirrors the Marriott/Starwood pattern directly: Najm's own legacy payment systems "
     "are still running under their pre-acquisition security standards. Data Classification, Cryptography, "
     "and Incident Response policies not yet extended. No unified monitoring across the combined estate. "
     "Third-Party & M&A Security Integration Policy (currently in Draft) is intended to formalize the "
     "timeline for closing this gap."),
    ("Regional Payment Gateway Partner", "Third-Party Partner", -400, 78,
     "Partner has agreed contractually to Falak Pay's Data Protection and Incident Response requirements; "
     "independent audit confirming actual implementation still pending."),
]


def get_or_create_policy(title, ptype, domain, owner, status, version, eff_offset, rev_offset, parent_title, notes, title_to_id):
    existing = a.Policy.query.filter_by(title=title).first()
    if existing:
        return existing, False
    parent_id = title_to_id.get(parent_title) if parent_title else None
    p = a.Policy(
        title=title, policy_type=ptype, domain=domain, owner=owner, status=status, version=version,
        effective_date=d(eff_offset) if eff_offset is not None else None,
        review_date=d(rev_offset) if rev_offset is not None else None,
        parent_id=parent_id, notes=notes,
    )
    a.db.session.add(p)
    a.db.session.commit()
    return p, True


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding Policy Register for Falak Pay Financial Company")
        print("=" * 70)
        title_to_id = {}
        # First pass: create policies without parents that are referenced later, in dependency order
        # (list is already ordered so masters/domain policies come before their children)
        for title, ptype, domain, owner, status, version, eff, rev, parent_title, notes in POLICIES:
            p, created = get_or_create_policy(title, ptype, domain, owner, status, version, eff, rev, parent_title, notes, title_to_id)
            title_to_id[title] = p.id
            flag = " ⚠ DELIBERATE OVERDUE REVIEW" if "OVERDUE" in (notes or "") else ""
            flag2 = " ⚠ MARRIOTT/STARWOOD GAP PATTERN" if "missing/delayed" in (notes or "") else ""
            print(f"  [{'CREATED' if created else 'exists'}] [{status:10s}] {title}{flag}{flag2}")

        print()
        print("=" * 70)
        print("Seeding M&A / Third-Entity Integration Register")
        print("=" * 70)
        if a.Entity.query.count() == 0:
            for name, etype, onboard_offset, pct, gap_notes in ENTITIES:
                a.db.session.add(a.Entity(
                    name=name, entity_type=etype,
                    acquired_or_onboarded_date=d(onboard_offset), integration_pct=pct, gap_notes=gap_notes,
                ))
                risk_flag = " ⚠ AT RISK (<70%)" if pct < 70 else ""
                print(f"  [{pct:3d}%] {name}{risk_flag}")
            a.db.session.commit()
        else:
            print("  Entities already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full Policy Framework demo dataset loaded")

        print()
        print("=" * 70)
        print("Done. Visit /dashboard for the coverage/integration overview,")
        print("/hierarchy for the policy tree, or /report for the full")
        print("board-ready Policy Framework document (printable to PDF).")
        print("Note: Cloud Security domain has NO policy seeded — a live gap")
        print("for the Coverage Gap Analysis module to demonstrate.")
        print("=" * 70)


if __name__ == "__main__":
    main()
