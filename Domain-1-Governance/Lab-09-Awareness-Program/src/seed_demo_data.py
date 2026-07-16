"""
Seed demo data for the Security Awareness & Training Program Tracker (Lab 09).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec awareness python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
import app as a

EMPLOYEES = [
    ("Yousef Al-Harbi", "Payments Operations", "Payments Officer", "2024-03-01", False),
    ("Fahad Al-Otaibi", "Payments Operations", "Payments Officer", "2024-06-15", False),
    ("Noura Al-Qahtani", "Payments Operations", "Head of Payments Operations", "2022-01-10", True),
    ("Sara Al-Dosari", "IT & Infrastructure", "IT Support Specialist", "2023-09-01", True),
    ("Omar Al-Shammari", "IT & Infrastructure", "Infrastructure Engineer", "2022-11-01", True),
    ("Fatimah Al-Zahrani", "IT & Infrastructure", "Head of Infrastructure & Vulnerability Mgmt", "2021-05-01", True),
    ("Khalid Al-Mutairi", "Executive", "CISO", "2021-01-01", True),
    ("Layla Al-Ghamdi", "Engineering", "Frontend Developer", "2023-02-01", False),
    ("Bilal Al-Rashid", "Engineering", "Backend Developer", "2024-01-15", False),
    ("Huda Al-Anazi", "Customer Support", "Support Team Lead", "2023-07-01", True),
    ("Mansour Al-Dawsari", "Customer Support", "Support Agent", "2025-01-05", False),
    ("Reem Al-Subai'i", "HR", "HR Coordinator", "2024-09-01", False),
]

COURSES = [
    ("Annual Cybersecurity Awareness", "All Staff", "Annual", "SAMA CSF 1.6"),
    ("Phishing Recognition & Reporting", "All Staff", "Annual", "SAMA CSF 1.6"),
    ("Vishing & Social Engineering Awareness", "All Staff", "Annual", "SAMA CSF 1.6 — Twitter 2020 case (see docs/case-study-twitter-breach.md)"),
    ("Secure Remote Work & Data Handling", "All Staff", "Annual", "SAMA CSF 1.6 / NCA TCC"),
    ("New Hire Security Induction", "All Staff", "Once (at hire)", "NCA ECC 1-10-6"),
    ("Secure Coding Fundamentals", "Developers", "Annual", "SAMA CSF 1.7 / NCA ECC 2-8"),
    ("Payment Fraud Awareness & Maker-Checker Discipline", "Payments Ops", "Annual", "SAMA CSF 3.7 — see Lab 02"),
    ("Privileged Access & Incident Response Fundamentals", "IT & Admins", "Annual", "SAMA CSF 1.7 / NCA ECC 2-2"),
]

# (employee_name, course_title, status, assigned_offset_days_ago, due_offset_days, completed_offset_days_ago)
ASSIGNMENTS = [
    # Yousef - mostly complete
    ("Yousef Al-Harbi", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-20"),
    ("Yousef Al-Harbi", "Phishing Recognition & Reporting", "Completed", "2026-01-05", "2026-02-05", "2026-01-22"),
    ("Yousef Al-Harbi", "Vishing & Social Engineering Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-25"),
    ("Yousef Al-Harbi", "Payment Fraud Awareness & Maker-Checker Discipline", "Completed", "2026-01-05", "2026-02-05", "2026-01-28"),

    # Noura - complete, privileged
    ("Noura Al-Qahtani", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-10"),
    ("Noura Al-Qahtani", "Vishing & Social Engineering Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-12"),
    ("Noura Al-Qahtani", "Privileged Access & Incident Response Fundamentals", "Completed", "2026-01-05", "2026-02-05", "2026-01-15"),

    # Sara - OVERDUE on vishing training (she's the one who failed the vishing sim, see below)
    ("Sara Al-Dosari", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-18"),
    ("Sara Al-Dosari", "Vishing & Social Engineering Awareness", "Overdue", "2026-01-05", "2026-02-05", None),
    ("Sara Al-Dosari", "Privileged Access & Incident Response Fundamentals", "In Progress", "2026-01-05", "2026-02-05", None),

    # Omar - complete
    ("Omar Al-Shammari", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-14"),
    ("Omar Al-Shammari", "Vishing & Social Engineering Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-16"),
    ("Omar Al-Shammari", "Privileged Access & Incident Response Fundamentals", "Completed", "2026-01-05", "2026-02-05", "2026-01-20"),

    # Fatimah - complete
    ("Fatimah Al-Zahrani", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-08"),
    ("Fatimah Al-Zahrani", "Vishing & Social Engineering Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-09"),

    # Khalid CISO - complete
    ("Khalid Al-Mutairi", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-06"),
    ("Khalid Al-Mutairi", "Vishing & Social Engineering Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-07"),

    # Layla - complete
    ("Layla Al-Ghamdi", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-19"),
    ("Layla Al-Ghamdi", "Secure Coding Fundamentals", "Completed", "2026-01-05", "2026-02-05", "2026-01-25"),

    # Bilal - new hire, in progress
    ("Bilal Al-Rashid", "New Hire Security Induction", "Completed", "2026-01-15", "2026-01-29", "2026-01-20"),
    ("Bilal Al-Rashid", "Annual Cybersecurity Awareness", "In Progress", "2026-01-15", "2026-02-15", None),
    ("Bilal Al-Rashid", "Secure Coding Fundamentals", "Not Started", "2026-01-15", "2026-03-01", None),

    # Huda - OVERDUE (repeat offender flagged below too)
    ("Huda Al-Anazi", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-30"),
    ("Huda Al-Anazi", "Vishing & Social Engineering Awareness", "Overdue", "2026-01-05", "2026-02-05", None),

    # Mansour - new-ish, in progress
    ("Mansour Al-Dawsari", "New Hire Security Induction", "Completed", "2026-01-10", "2026-01-24", "2026-01-15"),
    ("Mansour Al-Dawsari", "Phishing Recognition & Reporting", "In Progress", "2026-01-10", "2026-02-10", None),

    # Reem - complete
    ("Reem Al-Subai'i", "Annual Cybersecurity Awareness", "Completed", "2026-01-05", "2026-02-05", "2026-01-21"),
]

CAMPAIGNS = [
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Email Phishing", "2026-01-15",
     "Simulated email impersonating IT, asking employees to click a link and 'verify' their password before it expires."),
    ("Q2 2026 Email Phishing — Fake Invoice Attachment", "Email Phishing", "2026-04-10",
     "Simulated email with a malicious-looking invoice attachment, mimicking a vendor billing request."),
    ("Q1 2026 Vishing — Fake IT Support Credential Reset", "Vishing", "2026-02-20",
     "Simulated phone call impersonating IT support, asking the employee to 'confirm' their password or approve "
     "an access request to resolve a fake account lockout — directly modeled on the 2020 Twitter breach."),
]

# (campaign_name, employee_name, outcome, notes)
SIM_RESULTS = [
    # Q1 Email Phishing
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Yousef Al-Harbi", "Reported", "Reported to security team within 10 minutes."),
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Fahad Al-Otaibi", "Clicked - No Data Given", "Clicked the link but did not enter credentials on the fake page."),
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Noura Al-Qahtani", "Reported", ""),
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Sara Al-Dosari", "No Action", "Did not open the email."),
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Layla Al-Ghamdi", "Reported", ""),
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Bilal Al-Rashid", "Clicked - Credentials Given", "New hire, entered credentials on the fake reset page. Flagged for immediate follow-up training."),
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Huda Al-Anazi", "Clicked - No Data Given", ""),
    ("Q1 2026 Email Phishing — Fake IT Password Reset", "Mansour Al-Dawsari", "No Action", ""),

    # Q2 Email Phishing
    ("Q2 2026 Email Phishing — Fake Invoice Attachment", "Yousef Al-Harbi", "Reported", ""),
    ("Q2 2026 Email Phishing — Fake Invoice Attachment", "Fahad Al-Otaibi", "Reported", "Improved from Q1 — reported this time."),
    ("Q2 2026 Email Phishing — Fake Invoice Attachment", "Huda Al-Anazi", "Clicked - No Data Given",
     "Second failed simulation for this employee — see repeat-offender flag on Dashboard."),
    ("Q2 2026 Email Phishing — Fake Invoice Attachment", "Bilal Al-Rashid", "Reported", "Improved after Q1 follow-up training."),
    ("Q2 2026 Email Phishing — Fake Invoice Attachment", "Reem Al-Subai'i", "No Action", ""),
    ("Q2 2026 Email Phishing — Fake Invoice Attachment", "Mansour Al-Dawsari", "Clicked - No Data Given", ""),

    # Q1 Vishing — the Twitter-replay campaign
    ("Q1 2026 Vishing — Fake IT Support Credential Reset", "Noura Al-Qahtani", "Reported",
     "Correctly refused and reported the call to the security team — model response."),
    ("Q1 2026 Vishing — Fake IT Support Credential Reset", "Sara Al-Dosari", "Clicked - Credentials Given",
     "⚠ PRIVILEGED EMPLOYEE PROVIDED CREDENTIALS OVER THE PHONE to a caller impersonating IT support. "
     "This is a direct replay of the 2020 Twitter breach pattern — see docs/case-study-twitter-breach.md. "
     "Immediate mandatory retraining and process review required."),
    ("Q1 2026 Vishing — Fake IT Support Credential Reset", "Omar Al-Shammari", "No Action", "Hung up and independently called IT back to verify — correct response."),
    ("Q1 2026 Vishing — Fake IT Support Credential Reset", "Fatimah Al-Zahrani", "Reported", ""),
    ("Q1 2026 Vishing — Fake IT Support Credential Reset", "Khalid Al-Mutairi", "Reported", ""),
    ("Q1 2026 Vishing — Fake IT Support Credential Reset", "Huda Al-Anazi", "Clicked - No Data Given",
     "Engaged with the caller and described her role/access before growing suspicious and disengaging. Did not "
     "provide credentials but did not report the call either."),
]


def get_or_create_employee(name, dept, role, hire_date, privileged):
    existing = a.Employee.query.filter_by(name=name).first()
    if existing:
        return existing, False
    e = a.Employee(name=name, department=dept, role=role, hire_date=hire_date, is_privileged=privileged)
    a.db.session.add(e)
    a.db.session.commit()
    return e, True


def get_or_create_course(title, audience, frequency, maps_to):
    existing = a.Course.query.filter_by(title=title).first()
    if existing:
        return existing, False
    c = a.Course(title=title, audience=audience, frequency=frequency, maps_to=maps_to)
    a.db.session.add(c)
    a.db.session.commit()
    return c, True


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding Employee Roster for Falak Pay Financial Company")
        print("=" * 70)
        emp_map = {}
        for name, dept, role, hire_date, priv in EMPLOYEES:
            e, created = get_or_create_employee(name, dept, role, hire_date, priv)
            emp_map[name] = e
            flag = " [PRIVILEGED]" if priv else ""
            print(f"  [{'CREATED' if created else 'exists'}] {name} ({dept}){flag}")

        print()
        print("=" * 70)
        print("Seeding Training Course Catalog")
        print("=" * 70)
        course_map = {}
        for title, audience, freq, maps_to in COURSES:
            c, created = get_or_create_course(title, audience, freq, maps_to)
            course_map[title] = c
            print(f"  [{'CREATED' if created else 'exists'}] {title} ({audience})")

        print()
        print("=" * 70)
        print("Seeding Training Assignments")
        print("=" * 70)
        if a.TrainingAssignment.query.count() == 0:
            for emp_name, course_title, status, assigned, due, completed in ASSIGNMENTS:
                a.db.session.add(a.TrainingAssignment(
                    employee_id=emp_map[emp_name].id, course_id=course_map[course_title].id,
                    status=status, assigned_date=assigned, due_date=due, completed_date=completed,
                ))
            a.db.session.commit()
            print(f"  {len(ASSIGNMENTS)} training assignments created.")
        else:
            print("  Assignments already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Simulation Campaigns")
        print("=" * 70)
        campaign_map = {}
        if a.SimulationCampaign.query.count() == 0:
            for name, ctype, launch, desc in CAMPAIGNS:
                c = a.SimulationCampaign(name=name, campaign_type=ctype, launch_date=launch, scenario_description=desc)
                a.db.session.add(c)
                a.db.session.commit()
                campaign_map[name] = c
                print(f"  [{ctype:15s}] {name}")
        else:
            for name, *_ in CAMPAIGNS:
                campaign_map[name] = a.SimulationCampaign.query.filter_by(name=name).first()
            print("  Campaigns already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Simulation Results")
        print("=" * 70)
        if a.SimulationResult.query.count() == 0:
            for campaign_name, emp_name, outcome, notes in SIM_RESULTS:
                a.db.session.add(a.SimulationResult(
                    campaign_id=campaign_map[campaign_name].id, employee_id=emp_map[emp_name].id,
                    outcome=outcome, notes=notes,
                ))
                flag = " ⚠ TWITTER REPLAY" if "Twitter" in (notes or "") else ""
                print(f"  [{outcome:30s}] {emp_name} — {campaign_name[:40]}{flag}")
            a.db.session.commit()
        else:
            print("  Results already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full Awareness Program demo dataset loaded")

        print()
        print("=" * 70)
        print(f"Done. {a.Employee.query.count()} employees, {a.Course.query.count()} courses, "
              f"{a.TrainingAssignment.query.count()} assignments, {a.SimulationCampaign.query.count()} campaigns.")
        print("Visit /dashboard for the overview, or /report for the printable")
        print("audit-ready report.")
        print("=" * 70)


if __name__ == "__main__":
    main()
