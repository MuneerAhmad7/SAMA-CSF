"""
Security Awareness & Training Program Tracker — Lab 09 (Twitter 2020 scenario)

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///awareness.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

DEPARTMENTS = ["Payments Operations", "IT & Infrastructure", "Engineering", "Customer Support", "HR", "Executive"]
AUDIENCES = ["All Staff", "Payments Ops", "IT & Admins", "Developers", "Executives"]
TRAINING_STATUSES = ["Not Started", "In Progress", "Completed", "Overdue"]
CAMPAIGN_TYPES = ["Email Phishing", "Vishing", "Smishing"]
OUTCOMES = ["Reported", "No Action", "Clicked - No Data Given", "Clicked - Credentials Given"]
FAILURE_OUTCOMES = {"Clicked - No Data Given", "Clicked - Credentials Given"}


# ---------- Models ----------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(50))
    role = db.Column(db.String(100))
    hire_date = db.Column(db.String(20))
    is_privileged = db.Column(db.Boolean, default=False)

    assignments = db.relationship("TrainingAssignment", backref="employee", lazy=True)
    sim_results = db.relationship("SimulationResult", backref="employee", lazy=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    audience = db.Column(db.String(30))
    frequency = db.Column(db.String(20))
    maps_to = db.Column(db.String(100))

    assignments = db.relationship("TrainingAssignment", backref="course", lazy=True)


class TrainingAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    status = db.Column(db.String(20), default="Not Started")
    assigned_date = db.Column(db.String(20))
    due_date = db.Column(db.String(20))
    completed_date = db.Column(db.String(20))


class SimulationCampaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    campaign_type = db.Column(db.String(20))
    launch_date = db.Column(db.String(20))
    scenario_description = db.Column(db.Text)

    results = db.relationship("SimulationResult", backref="campaign", lazy=True)


class SimulationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("simulation_campaign.id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    outcome = db.Column(db.String(40))
    notes = db.Column(db.String(300))


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    actor = db.Column(db.String(100))
    action = db.Column(db.String(80))
    details = db.Column(db.String(400))


def log(actor, action, details=""):
    db.session.add(AuditLog(actor=actor, action=action, details=details))
    db.session.commit()


def init_db():
    db.create_all()


def training_completion_pct():
    assignments = TrainingAssignment.query.all()
    if not assignments:
        return 0
    completed = len([a for a in assignments if a.status == "Completed"])
    return round((completed / len(assignments)) * 100, 1)


def repeat_offenders():
    """Employees who failed (clicked) in 2+ simulation campaigns."""
    employees = Employee.query.all()
    offenders = []
    for e in employees:
        failures = [r for r in e.sim_results if r.outcome in FAILURE_OUTCOMES]
        if len(failures) >= 2:
            offenders.append((e, failures))
    return offenders


def privileged_vishing_failures():
    """The Twitter-specific risk flag: privileged employees who failed a vishing sim."""
    results = SimulationResult.query.join(SimulationCampaign).filter(
        SimulationCampaign.campaign_type == "Vishing",
        SimulationResult.outcome.in_(FAILURE_OUTCOMES),
    ).all()
    return [r for r in results if r.employee and r.employee.is_privileged]


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    employees = Employee.query.all()
    assignments = TrainingAssignment.query.all()
    campaigns = SimulationCampaign.query.all()

    completion_pct = training_completion_pct()
    overdue = [a for a in assignments if a.status == "Overdue"]
    offenders = repeat_offenders()
    priv_vishing_fails = privileged_vishing_failures()

    campaign_stats = []
    for c in campaigns:
        total = len(c.results)
        failed = len([r for r in c.results if r.outcome in FAILURE_OUTCOMES])
        reported = len([r for r in c.results if r.outcome == "Reported"])
        fail_rate = round((failed / total) * 100, 1) if total else 0
        report_rate = round((reported / total) * 100, 1) if total else 0
        campaign_stats.append({"campaign": c, "total": total, "failed": failed, "fail_rate": fail_rate,
                                "reported": reported, "report_rate": report_rate})

    return render_template(
        "dashboard.html", employee_count=len(employees), completion_pct=completion_pct,
        overdue_count=len(overdue), overdue=overdue, offenders=offenders,
        priv_vishing_fails=priv_vishing_fails, campaign_stats=campaign_stats,
    )


@app.route("/employees", methods=["GET", "POST"])
def employees():
    if request.method == "POST":
        e = Employee(
            name=request.form["name"], department=request.form["department"],
            role=request.form.get("role"), hire_date=request.form.get("hire_date"),
            is_privileged="is_privileged" in request.form,
        )
        db.session.add(e)
        db.session.commit()
        log("Awareness Program Owner", "EMPLOYEE_ADDED", f"id={e.id} name={e.name}")
        flash("Employee added.")
        return redirect(url_for("employees"))
    return render_template("employees.html", employees=Employee.query.all(), departments=DEPARTMENTS)


@app.route("/training", methods=["GET", "POST"])
def training():
    if request.method == "POST":
        a = TrainingAssignment(
            employee_id=int(request.form["employee_id"]), course_id=int(request.form["course_id"]),
            status="Not Started", assigned_date=request.form.get("assigned_date"),
            due_date=request.form.get("due_date"),
        )
        db.session.add(a)
        db.session.commit()
        log("Awareness Program Owner", "TRAINING_ASSIGNED",
            f"employee_id={a.employee_id} course_id={a.course_id}")
        flash("Training assigned.")
        return redirect(url_for("training"))
    return render_template(
        "training.html", assignments=TrainingAssignment.query.all(),
        employees=Employee.query.all(), courses=Course.query.all(), statuses=TRAINING_STATUSES,
    )


@app.route("/training/<int:assignment_id>/update", methods=["POST"])
def update_training(assignment_id):
    a = TrainingAssignment.query.get_or_404(assignment_id)
    old_status = a.status
    a.status = request.form["status"]
    if a.status == "Completed" and not a.completed_date:
        a.completed_date = request.form.get("completed_date") or datetime.utcnow().strftime("%Y-%m-%d")
    db.session.commit()
    log("Awareness Program Owner", "TRAINING_STATUS_CHANGED",
        f"id={a.id} employee={a.employee.name if a.employee else '?'} course={a.course.title if a.course else '?'} {old_status} -> {a.status}")
    flash(f"Training updated: {old_status} → {a.status}")
    return redirect(url_for("training"))


@app.route("/simulations")
def simulations():
    campaigns = SimulationCampaign.query.all()
    return render_template("simulations.html", campaigns=campaigns, failure_outcomes=FAILURE_OUTCOMES)


@app.route("/courses")
def courses():
    return render_template("courses.html", courses=Course.query.all())


@app.route("/audit")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    employees_list = Employee.query.all()
    courses_list = Course.query.all()
    campaigns = SimulationCampaign.query.all()
    completion_pct = training_completion_pct()
    offenders = repeat_offenders()
    priv_vishing_fails = privileged_vishing_failures()

    campaign_stats = []
    for c in campaigns:
        total = len(c.results)
        failed = len([r for r in c.results if r.outcome in FAILURE_OUTCOMES])
        fail_rate = round((failed / total) * 100, 1) if total else 0
        campaign_stats.append({"campaign": c, "total": total, "failed": failed, "fail_rate": fail_rate})

    return render_template(
        "report.html", employees=employees_list, courses=courses_list, completion_pct=completion_pct,
        offenders=offenders, priv_vishing_fails=priv_vishing_fails, campaign_stats=campaign_stats,
        generated_at=datetime.utcnow(),
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5008, debug=True)
