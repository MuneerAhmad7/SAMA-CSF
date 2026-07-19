"""
Seed demo data for the Security Team Training & Certification Plan Tracker (Lab 13).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec training-plan python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
from datetime import datetime, timedelta

import app as a

now = datetime.utcnow()


def d(days_offset):
    return (now + timedelta(days=days_offset)).strftime("%Y-%m-%d")


MEMBERS = [
    ("Khalid Al-Mutairi", "CISO", -1800),
    ("Sara Al-Dosari", "SOC Analyst", -900),
    ("Omar Al-Shammari", "Security Engineer", -1400),
    ("Fatimah Al-Zahrani", "Incident Responder", -1600),
    ("Yousef Bin-Nasser", "Penetration Tester", -600),
    ("Huda Al-Anazi", "GRC Analyst", -700),
]

# (member_name, skill_name, current_level, required_level, assessed_offset_days_ago, notes)
SKILL_ASSESSMENTS = [
    ("Khalid Al-Mutairi", "GRC / Audit", 4, 4, -60, "Strong, consistent with CISO role."),
    ("Khalid Al-Mutairi", "Incident Response", 3, 3, -60, ""),

    ("Sara Al-Dosari", "Incident Response", 2, 3, -60, "Developing — see training plan."),
    ("Sara Al-Dosari", "Cloud Security", 1, 2, -60, ""),
    ("Sara Al-Dosari", "Digital Forensics", 1, 3, -60,
     "⚠ SIGNIFICANT GAP. Flagged in the FY2025 Internal Cybersecurity Audit (see Lab 11) as a technical "
     "capability weakness on the SOC team. No funded training plan existed to close this gap as of the "
     "prior assessment cycle — directly mirroring the OPM pattern of a repeatedly identified but unaddressed "
     "capability gap. See docs/case-study-opm-breach.md."),

    ("Omar Al-Shammari", "Cloud Security", 2, 3, -60, "Improving after CSPM rollout (see Lab 07)."),
    ("Omar Al-Shammari", "Incident Response", 3, 3, -60, ""),
    ("Omar Al-Shammari", "Secure Code Review", 1, 2, -60, ""),

    ("Fatimah Al-Zahrani", "Incident Response", 4, 4, -60, "Deep expertise, mentors the team."),
    ("Fatimah Al-Zahrani", "Digital Forensics", 3, 4, -60, "Strong but organization still under-resourced overall — see Sara's gap above."),
    ("Fatimah Al-Zahrani", "Cloud Security", 2, 3, -60, ""),

    ("Yousef Bin-Nasser", "Penetration Testing", 3, 4, -60, "On track — OSCP prep underway, see Training Plan."),
    ("Yousef Bin-Nasser", "Secure Code Review", 2, 3, -60, ""),

    ("Huda Al-Anazi", "GRC / Audit", 3, 3, -60, ""),
    ("Huda Al-Anazi", "Incident Response", 1, 2, -60, ""),
]

# (member_name, cert_name, issuer, issued_offset_days, expiry_offset_days, required)
CERTIFICATIONS = [
    ("Khalid Al-Mutairi", "CISSP", "(ISC)²", -900, 265, True),
    ("Khalid Al-Mutairi", "CISM", "ISACA", -600, 500, True),
    ("Fatimah Al-Zahrani", "GCFA (Certified Forensic Analyst)", "GIAC", -700, 30, True),  # Expiring Soon
    ("Fatimah Al-Zahrani", "CISSP", "(ISC)²", -1000, -20, True),  # Expired
    ("Omar Al-Shammari", "CCSP (Cloud Security)", "(ISC)²", -300, 700, True),
    ("Sara Al-Dosari", "GCIH (Incident Handler)", "GIAC", -400, 320, False),
    ("Yousef Bin-Nasser", "OSCP", "Offensive Security", -200, 900, True),
    ("Huda Al-Anazi", "CISA", "ISACA", -500, 600, True),
]

# (title, member_name, plan_type, target_skill_name, budget, target_offset_days, status, notes)
PLAN_ITEMS = [
    ("GCFA Digital Forensics Certification Prep", "Sara Al-Dosari", "Certification Prep", "Digital Forensics",
     8500, 90, "Planned",
     "Directly targets the Critical Digital Forensics gap flagged above and cross-referenced with Lab 11's "
     "audit finding. This is the funded plan item that, per the OPM case study, should exist as soon as a "
     "capability gap is identified — not years later."),
    ("AWS/Azure Cloud Security Workshop", "Sara Al-Dosari", "Workshop", "Cloud Security", 2000, 45, "In Progress", ""),
    ("OSCP Exam Retake Preparation", "Yousef Bin-Nasser", "Certification Prep", "Penetration Testing", 1500, 30, "In Progress", ""),
    ("Secure Code Review Bootcamp", "Omar Al-Shammari", "Formal Course", "Secure Code Review", 3000, 60, "Planned", ""),
    ("SANS Cloud Security Conference", "Omar Al-Shammari", "Conference", "Cloud Security", 6000, 120, "Delayed",
     "Budget approval delayed pending Q2 review — see training plan status."),
    ("CISSP Renewal CPE Credits", "Khalid Al-Mutairi", "Formal Course", None, 500, 200, "Completed", "Annual CPE requirement met."),
    ("Incident Response Tabletop Facilitation Training", "Huda Al-Anazi", "Workshop", "Incident Response", 1200, 75, "Planned", ""),
    ("GCFA Recertification", "Fatimah Al-Zahrani", "Certification Prep", "Digital Forensics", 1000, 20, "In Progress",
     "Renewing ahead of the Expiring Soon deadline flagged in Certifications."),
]


def get_or_create_member(name, role, hire_offset):
    existing = a.TeamMember.query.filter_by(name=name).first()
    if existing:
        return existing, False
    m = a.TeamMember(name=name, role=role, hire_date=d(hire_offset))
    a.db.session.add(m)
    a.db.session.commit()
    return m, True


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding Security Team Roster for Falak Pay Financial Company")
        print("=" * 70)
        member_map = {}
        for name, role, hire_offset in MEMBERS:
            m, created = get_or_create_member(name, role, hire_offset)
            member_map[name] = m
            print(f"  [{'CREATED' if created else 'exists'}] {name} ({role})")

        skill_map = {s.name: s for s in a.Skill.query.all()}
        print(f"\n  {len(skill_map)} skill specialties available: {', '.join(skill_map.keys())}")

        print()
        print("=" * 70)
        print("Seeding Skills Matrix")
        print("=" * 70)
        if a.SkillAssessment.query.count() == 0:
            for member_name, skill_name, current, required, assessed_offset, notes in SKILL_ASSESSMENTS:
                a.db.session.add(a.SkillAssessment(
                    member_id=member_map[member_name].id, skill_id=skill_map[skill_name].id,
                    current_level=current, required_level=required, assessed_date=d(assessed_offset), notes=notes,
                ))
                gap = required - current
                flag = " ⚠ OPM PATTERN GAP" if "OPM" in (notes or "") else (" ⚠ GAP" if gap > 0 else "")
                print(f"  [{current}/{required}] {member_name} — {skill_name}{flag}")
            a.db.session.commit()
        else:
            print("  Skills matrix already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Certification Register")
        print("=" * 70)
        if a.Certification.query.count() == 0:
            for member_name, cert_name, issuer, issued_offset, expiry_offset, required in CERTIFICATIONS:
                a.db.session.add(a.Certification(
                    member_id=member_map[member_name].id, name=cert_name, issuer=issuer,
                    issued_date=d(issued_offset), expiry_date=d(expiry_offset), required_for_role=required,
                ))
                status_flag = "EXPIRED" if expiry_offset < 0 else ("EXPIRING SOON" if expiry_offset <= 90 else "Active")
                print(f"  [{status_flag:14s}] {member_name} — {cert_name}")
            a.db.session.commit()
        else:
            print("  Certifications already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Training Plan")
        print("=" * 70)
        if a.TrainingPlanItem.query.count() == 0:
            for title, member_name, ptype, skill_name, budget, target_offset, status, notes in PLAN_ITEMS:
                a.db.session.add(a.TrainingPlanItem(
                    member_id=member_map[member_name].id, title=title, plan_type=ptype,
                    target_skill_id=skill_map[skill_name].id if skill_name else None,
                    budget=budget, target_date=d(target_offset), status=status, notes=notes,
                ))
                print(f"  [{status:12s}] {title} (SAR {budget:,.0f})")
            a.db.session.commit()
        else:
            print("  Training plan already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full Training & Certification Plan demo dataset loaded")

        print()
        print("=" * 70)
        print(f"Done. {a.TeamMember.query.count()} team members, {a.SkillAssessment.query.count()} skill "
              f"assessments, {a.Certification.query.count()} certifications, {a.TrainingPlanItem.query.count()} "
              f"training plan items seeded.")
        print("Visit /dashboard for the overview, or /report for the printable")
        print("audit-ready report.")
        print("=" * 70)


if __name__ == "__main__":
    main()
