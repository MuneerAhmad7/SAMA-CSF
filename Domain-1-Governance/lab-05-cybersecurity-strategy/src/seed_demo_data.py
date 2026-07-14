"""
Seed demo data for the Cybersecurity Strategy Builder (Lab 05).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec strategy-tracker python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
import app as a

STRATEGY_DATA = {
    "organization_name": "Falak Pay Financial Company",
    "vision_statement": (
        "By 2029, Falak Pay operates a cybersecurity program at SAMA CSF Maturity Level 4 (Managed) "
        "across all domains, with security treated as a funded, board-owned strategic priority rather "
        "than a reactive cost center — a lesson drawn directly from the 2014 Sony Pictures breach, "
        "where underinvestment following an earlier major incident contributed to a second, more "
        "damaging one three years later."
    ),
    "strategic_period": "2026 - 2029",
    "business_alignment": (
        "This strategy directly supports Falak Pay's growth into new payment corridors by ensuring "
        "customer trust and regulatory standing are protected as transaction volumes scale. Security "
        "maturity targets are tied to specific business milestones (new market entry, new product "
        "launches) rather than treated as a parallel, disconnected workstream."
    ),
    "threat_landscape_summary": (
        "Key threats considered: organized financial fraud rings targeting payment rails (High/High); "
        "nation-state or hacktivist actors motivated by geopolitical events involving Saudi financial "
        "institutions (Medium/High — informed directly by the Sony Pictures case, where a foreseeable "
        "geopolitical trigger was not reflected in defensive posture); ransomware targeting core banking "
        "infrastructure (Medium/High); third-party/supply-chain compromise (Medium/Medium); insider "
        "threat in payments operations (Low/High)."
    ),
    "total_budget": "18,500,000",
    "review_cycle": "Annual, with mandatory re-assessment following any Critical incident or major geopolitical/threat landscape shift",
    "approved_by": "Falak Pay Board Risk & Compliance Committee",
    "approval_date": "1 May 2026",
}

MATURITY_SCORES = {
    "Governance & Leadership": (3, 4, "CISO Charter in place (see Lab 04); Committee cadence still maturing"),
    "Risk Management": (2, 4, "Risk register exists but lacks continuous monitoring integration"),
    "Identity & Access Management": (3, 4, "MFA + maker-checker live in SecurePay (Lab 02); PAM tooling not yet org-wide"),
    "Network & Infrastructure Security": (2, 4, "Segmentation partial; SIEM deployed but not fully tuned"),
    "Application Security": (2, 3, "SSDLC defined but SAST/DAST not yet mandatory gate in CI/CD"),
    "Data Protection": (2, 4, "Classification scheme exists; DLP not yet deployed org-wide"),
    "Incident Response": (3, 4, "IR plan tested via tabletop; SOC coverage not yet 24/7"),
    "Third-Party & Cloud Security": (1, 3, "No formal CSPM tooling; vendor risk assessments inconsistent"),
    "Business Continuity": (2, 3, "BCP documented; DR testing not yet annual-cadence proven"),
    "Security Awareness & Training": (3, 4, "Annual training + phishing sims running; role-based training incomplete"),
}

THREATS = [
    ("Organized Financial Fraud", "Fraud rings targeting payment rails and account takeover", "High", "High",
     "Directly relevant given SecurePay's transaction volumes — see Lab 02 fraud engine"),
    ("Nation-State / Geopolitical", "State-linked or hacktivist actors reacting to geopolitical events",
     "Medium", "High",
     "The exact blind spot in the Sony Pictures 2014 case — a foreseeable trigger not reflected in posture. "
     "Falak Pay's strategy explicitly tracks this category as a result."),
    ("Ransomware", "Encryption/extortion targeting core banking or payment infrastructure", "Medium", "High",
     "Would directly threaten Payment Switch Server and Core Banking Database (see Lab 03 asset inventory)"),
    ("Third-Party / Supply Chain Compromise", "Compromise via vendor or software supply chain", "Medium", "Medium",
     "Relevant given reliance on external payment gateway and cloud providers"),
    ("Insider Threat — Payments Operations", "Malicious or negligent insider with payment system access",
     "Low", "High", "Mitigated partially by maker-checker SoD (Lab 02) but not eliminated"),
    ("Unpatched Known Vulnerabilities", "Known CVEs left unpatched past SLA", "Medium", "High",
     "Directly demonstrated by the Equifax-pattern finding in Lab 03"),
]

INITIATIVES = [
    # Foundation phase
    ("Formalize CISO Charter & Authority", "Foundation", "Governance & Leadership", "Khalid Al-Mutairi", 50000, 50000, "Completed", "Q1 2026"),
    ("Complete Enterprise Risk Register", "Foundation", "Risk Management", "Fatimah Al-Zahrani", 80000, 80000, "Completed", "Q1 2026"),
    ("Deploy MFA + Maker-Checker on Payment Systems", "Foundation", "Identity & Access Management", "Noura Al-Qahtani", 350000, 320000, "Completed", "Q1 2026"),
    ("Establish Vulnerability Management SLA Program", "Foundation", "Network & Infrastructure Security", "Fatimah Al-Zahrani", 200000, 200000, "Completed", "Q2 2026"),

    # Core Controls phase
    ("Org-wide SIEM Deployment & Tuning", "Core Controls", "Network & Infrastructure Security", "Omar Al-Shammari", 900000, 450000, "In Progress", "Q3 2026"),
    ("SSDLC Gate: Mandatory SAST/DAST in CI/CD", "Core Controls", "Application Security", "Layla Al-Ghamdi", 400000, 100000, "In Progress", "Q3 2026"),
    ("Data Classification & DLP Rollout", "Core Controls", "Data Protection", "Fatimah Al-Zahrani", 600000, 0, "Not Started", "Q4 2026"),
    ("24/7 SOC Coverage (in-house + MSSP hybrid)", "Core Controls", "Incident Response", "Noura Al-Qahtani", 1200000, 300000, "In Progress", "Q4 2026"),
    ("Annual DR Test Program Formalization", "Core Controls", "Business Continuity", "Omar Al-Shammari", 250000, 0, "Delayed", "Q2 2026"),

    # Advanced Controls phase
    ("Cloud Security Posture Management (CSPM) Deployment", "Advanced Controls", "Third-Party & Cloud Security", "Omar Al-Shammari", 500000, 0, "Not Started", "Q1 2027"),
    ("Third-Party Risk Automation Platform", "Advanced Controls", "Third-Party & Cloud Security", "Khalid Al-Mutairi", 350000, 0, "Not Started", "Q2 2027"),
    ("Role-Based Security Awareness Program", "Advanced Controls", "Security Awareness & Training", "Layla Al-Ghamdi", 150000, 20000, "In Progress", "Q1 2027"),
    ("Zero Trust Architecture Pilot", "Advanced Controls", "Network & Infrastructure Security", "Fatimah Al-Zahrani", 800000, 0, "Not Started", "Q3 2027"),

    # Optimization phase
    ("Continuous Compliance Monitoring & Automated Evidence", "Optimization", "Governance & Leadership", "Khalid Al-Mutairi", 400000, 0, "Not Started", "Q1 2028"),
]


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding Cybersecurity Strategy for Falak Pay Financial Company")
        print("=" * 70)
        for key, value in STRATEGY_DATA.items():
            field = a.StrategyField.query.filter_by(field_key=key).first()
            if field:
                print(f"  [exists] {key}")
                continue
            a.db.session.add(a.StrategyField(field_key=key, value=value))
            print(f"  [SET] {key}")
        a.db.session.commit()

        print()
        print("=" * 70)
        print("Scoring Maturity Assessment (10 domains)")
        print("=" * 70)
        for domain, (current, target, notes) in MATURITY_SCORES.items():
            s = a.MaturityScore.query.filter_by(domain=domain).first()
            if s:
                s.current_level = current
                s.target_level = target
                s.notes = notes
                print(f"  [{current} -> {target}] {domain}")
        a.db.session.commit()

        print()
        print("=" * 70)
        print("Seeding Threat Landscape Register")
        print("=" * 70)
        if a.ThreatItem.query.count() == 0:
            for threat_type, desc, likelihood, impact, notes in THREATS:
                a.db.session.add(a.ThreatItem(
                    threat_type=threat_type, description=desc, likelihood=likelihood,
                    impact=impact, relevance_notes=notes,
                ))
                score = a.risk_score(likelihood, impact)
                flag = " ⚠ HIGH RISK" if score >= 6 else ""
                print(f"  [score={score}] {threat_type}{flag}")
            a.db.session.commit()
        else:
            print("  Threats already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Strategic Roadmap (14 initiatives across 4 phases)")
        print("=" * 70)
        if a.Initiative.query.count() == 0:
            for title, phase, domain, owner, allocated, spent, status, quarter in INITIATIVES:
                a.db.session.add(a.Initiative(
                    title=title, phase=phase, domain=domain, owner=owner,
                    budget_allocated=allocated, budget_spent=spent, status=status, target_quarter=quarter,
                ))
                print(f"  [{phase:16s}] {title} -> {status}")
            a.db.session.commit()
        else:
            print("  Initiatives already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full Cybersecurity Strategy demo dataset loaded")

        print()
        print("=" * 70)
        print("Done. Visit /dashboard for the maturity/budget overview, or /report")
        print("for the full board-ready Strategy document (printable to PDF).")
        print("=" * 70)


if __name__ == "__main__":
    main()
