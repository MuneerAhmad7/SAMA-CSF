"""
Governance & Compliance Tracker
Lab 01 - SAMA CSF / NCA ECC Domain 1 (Governance)

A small, self-contained Flask + SQLite app for tracking:
- Cybersecurity policies (lifecycle: Draft -> Under Review -> Approved -> Published)
- RACI matrix entries
- Cyber Security Committee / Board meetings
- KPIs / KRIs with RAG status
- Compliance checklist (pre-seeded with SAMA CSF 1.1-1.9 and NCA ECC 1-1..1-10 controls)

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///governance.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)


# ---------- Models ----------
class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    owner = db.Column(db.String(120))
    status = db.Column(db.String(30), default="Draft")  # Draft/Under Review/Approved/Published
    version = db.Column(db.String(10), default="0.1")
    review_date = db.Column(db.Date)
    notes = db.Column(db.Text)


class RaciEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(200), nullable=False)
    responsible = db.Column(db.String(120))
    accountable = db.Column(db.String(120))
    consulted = db.Column(db.String(120))
    informed = db.Column(db.String(120))


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_date = db.Column(db.Date, default=date.today)
    attendees = db.Column(db.String(300))
    agenda = db.Column(db.Text)
    decisions = db.Column(db.Text)
    action_items = db.Column(db.Text)


class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    target = db.Column(db.String(50))
    actual = db.Column(db.String(50))
    status = db.Column(db.String(10), default="Amber")  # Green/Amber/Red


class ComplianceControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    framework = db.Column(db.String(20))       # SAMA CSF / NCA ECC
    control_id = db.Column(db.String(20))
    description = db.Column(db.String(300))
    status = db.Column(db.String(20), default="Not Implemented")  # Implemented/Partial/Not Implemented
    evidence = db.Column(db.String(300))


# ---------- Seed data ----------
DOMAIN1_CONTROLS = [
    ("SAMA CSF", "1.1", "Cyber Security Governance Structure (CISO, Committee, reporting lines)"),
    ("SAMA CSF", "1.2", "Cyber Security Strategy (3-5yr, annual review, budget, KPIs)"),
    ("SAMA CSF", "1.3", "Cyber Security Policy (Board approved, communicated, acknowledged)"),
    ("SAMA CSF", "1.4", "Roles and Responsibilities (RACI, segregation of duties)"),
    ("SAMA CSF", "1.5", "Cyber Security in Project Management (gates, sign-off)"),
    ("SAMA CSF", "1.6", "Cyber Security Awareness (annual, phishing sims quarterly)"),
    ("SAMA CSF", "1.7", "Cyber Security Training (certifications, needs assessment)"),
    ("SAMA CSF", "1.8", "Cyber Security Review and Audit (internal/external, pentest, vuln mgmt)"),
    ("SAMA CSF", "1.9", "Regulatory Compliance (SAMA/PCI-DSS/SWIFT CSP)"),
    ("NCA ECC", "1-1", "Cybersecurity Strategy established, approved, communicated, reviewed"),
    ("NCA ECC", "1-2", "Cybersecurity Management function, leader, committee, resources, independence"),
    ("NCA ECC", "1-3", "Cybersecurity Policies and Procedures"),
    ("NCA ECC", "1-4", "Cybersecurity Roles and Responsibilities"),
    ("NCA ECC", "1-5", "Cybersecurity Risk Management"),
    ("NCA ECC", "1-6", "Cybersecurity in IT Projects"),
    ("NCA ECC", "1-7", "Compliance with Standards, Laws and Regulations"),
    ("NCA ECC", "1-8", "Periodic Cybersecurity Review and Audit"),
    ("NCA ECC", "1-9", "Cybersecurity in Human Resources"),
    ("NCA ECC", "1-10", "Cybersecurity Awareness and Training"),
]

SAMPLE_RACI = [
    ("Approve cybersecurity strategy", "CISO", "Board Committee", "IT/Legal", "All Staff"),
    ("Approve cybersecurity policy", "CISO", "Board Committee", "IT/Legal", "All Staff"),
    ("Conduct annual risk assessment", "CISO/GRC Team", "CISO", "IT Ops/Legal", "Board"),
    ("Board cybersecurity reporting", "CISO", "Board Committee", "-", "All Staff"),
]


def seed():
    if ComplianceControl.query.count() == 0:
        for fw, cid, desc in DOMAIN1_CONTROLS:
            db.session.add(ComplianceControl(framework=fw, control_id=cid, description=desc))
    if RaciEntry.query.count() == 0:
        for act, r, a, c, i in SAMPLE_RACI:
            db.session.add(RaciEntry(activity=act, responsible=r, accountable=a, consulted=c, informed=i))
    db.session.commit()


# ---------- Routes ----------
@app.route("/")
def dashboard():
    total = ComplianceControl.query.count()
    implemented = ComplianceControl.query.filter_by(status="Implemented").count()
    partial = ComplianceControl.query.filter_by(status="Partial").count()
    compliance_pct = round(((implemented + 0.5 * partial) / total) * 100, 1) if total else 0

    today = date.today()
    overdue_policies = Policy.query.filter(Policy.review_date < today).count()
    metrics = Metric.query.all()

    return render_template(
        "dashboard.html",
        compliance_pct=compliance_pct,
        total=total,
        implemented=implemented,
        partial=partial,
        overdue_policies=overdue_policies,
        policies_count=Policy.query.count(),
        meetings_count=Meeting.query.count(),
        metrics=metrics,
    )


@app.route("/policies", methods=["GET", "POST"])
def policies():
    if request.method == "POST":
        p = Policy(
            title=request.form["title"],
            owner=request.form["owner"],
            status=request.form["status"],
            version=request.form["version"],
            review_date=datetime.strptime(request.form["review_date"], "%Y-%m-%d").date()
            if request.form["review_date"] else None,
            notes=request.form.get("notes"),
        )
        db.session.add(p)
        db.session.commit()
        flash("Policy saved.")
        return redirect(url_for("policies"))
    return render_template("policies.html", policies=Policy.query.all(), today=date.today())


@app.route("/raci", methods=["GET", "POST"])
def raci():
    if request.method == "POST":
        r = RaciEntry(
            activity=request.form["activity"],
            responsible=request.form["responsible"],
            accountable=request.form["accountable"],
            consulted=request.form["consulted"],
            informed=request.form["informed"],
        )
        db.session.add(r)
        db.session.commit()
        flash("RACI entry saved.")
        return redirect(url_for("raci"))
    return render_template("raci.html", entries=RaciEntry.query.all())


@app.route("/meetings", methods=["GET", "POST"])
def meetings():
    if request.method == "POST":
        m = Meeting(
            meeting_date=datetime.strptime(request.form["meeting_date"], "%Y-%m-%d").date(),
            attendees=request.form["attendees"],
            agenda=request.form["agenda"],
            decisions=request.form["decisions"],
            action_items=request.form["action_items"],
        )
        db.session.add(m)
        db.session.commit()
        flash("Meeting logged.")
        return redirect(url_for("meetings"))
    return render_template("meetings.html", meetings=Meeting.query.order_by(Meeting.meeting_date.desc()).all())


@app.route("/metrics", methods=["GET", "POST"])
def metrics():
    if request.method == "POST":
        m = Metric(
            name=request.form["name"],
            target=request.form["target"],
            actual=request.form["actual"],
            status=request.form["status"],
        )
        db.session.add(m)
        db.session.commit()
        flash("Metric saved.")
        return redirect(url_for("metrics"))
    return render_template("metrics.html", metrics=Metric.query.all())


@app.route("/compliance", methods=["GET", "POST"])
def compliance():
    if request.method == "POST":
        control = ComplianceControl.query.get(request.form["control_id"])
        control.status = request.form["status"]
        control.evidence = request.form["evidence"]
        db.session.commit()
        flash("Control updated.")
        return redirect(url_for("compliance"))
    return render_template("compliance.html", controls=ComplianceControl.query.all())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed()
    app.run(host="0.0.0.0", port=5000, debug=True)
