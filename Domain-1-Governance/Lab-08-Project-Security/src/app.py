"""
Project Security Gate Tracker — Lab 08 (British Airways 2018 scenario)

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projectsecurity.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

PROJECT_TYPES = ["New Application", "Feature Enhancement", "Third-Party Integration", "Infrastructure Change"]
CRITICALITIES = ["Critical", "High", "Medium", "Low"]
GATE_NAMES = ["Initiation", "Design", "Build", "Test", "Deploy", "Post-Implementation"]
GATE_STATUSES = ["Not Started", "In Progress", "Passed", "Failed", "Waived"]
RISK_LEVELS = ["Critical", "High", "Medium", "Low"]


# ---------- Models ----------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    project_type = db.Column(db.String(30))
    business_unit = db.Column(db.String(100))
    criticality = db.Column(db.String(20))
    owner = db.Column(db.String(100))
    current_phase = db.Column(db.String(30), default="Initiation")

    gates = db.relationship("SecurityGate", backref="project", lazy=True)
    changes = db.relationship("ChangeRecord", backref="project", lazy=True)


class SecurityGate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    gate_name = db.Column(db.String(30))
    status = db.Column(db.String(20), default="Not Started")
    approver = db.Column(db.String(100))
    gate_date = db.Column(db.String(20))
    evidence_notes = db.Column(db.Text)


class ThirdPartyScript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    page_context = db.Column(db.String(150))
    source_url = db.Column(db.String(300))
    sri_pinned = db.Column(db.Boolean, default=False)
    last_reviewed = db.Column(db.String(20))
    risk_level = db.Column(db.String(20))
    notes = db.Column(db.Text)


class ChangeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=True)
    title = db.Column(db.String(200))
    change_type = db.Column(db.String(50))
    deployed_at = db.Column(db.String(20))
    gate_passed = db.Column(db.Boolean, default=True)
    approver = db.Column(db.String(100))
    notes = db.Column(db.Text)


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


def project_gate_compliance(project):
    gates = project.gates
    if not gates:
        return 0
    passed = len([g for g in gates if g.status == "Passed"])
    return round((passed / len(gates)) * 100, 1)


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    projects = Project.query.all()
    gates = SecurityGate.query.all()
    scripts = ThirdPartyScript.query.all()
    changes = ChangeRecord.query.all()

    total_gates = len(gates)
    passed_gates = len([g for g in gates if g.status == "Passed"])
    failed_or_waived = [g for g in gates if g.status in ("Failed", "Waived")]
    overall_compliance = round((passed_gates / total_gates) * 100, 1) if total_gates else 0

    unprotected_scripts = [s for s in scripts if not s.sri_pinned]
    sensitive_unprotected = [s for s in unprotected_scripts if s.risk_level in ("Critical", "High")]

    ungated_changes = [c for c in changes if not c.gate_passed]

    project_scores = [(p, project_gate_compliance(p)) for p in projects]
    lowest_compliance = sorted(project_scores, key=lambda x: x[1])[:3]

    return render_template(
        "dashboard.html", project_count=len(projects), total_gates=total_gates, passed_gates=passed_gates,
        overall_compliance=overall_compliance, failed_or_waived=failed_or_waived,
        unprotected_scripts=unprotected_scripts, sensitive_unprotected=sensitive_unprotected,
        ungated_changes=ungated_changes, lowest_compliance=lowest_compliance,
    )


@app.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        p = Project(
            name=request.form["name"], project_type=request.form["project_type"],
            business_unit=request.form.get("business_unit"), criticality=request.form["criticality"],
            owner=request.form.get("owner"), current_phase="Initiation",
        )
        db.session.add(p)
        db.session.commit()
        for gate_name in GATE_NAMES:
            db.session.add(SecurityGate(project_id=p.id, gate_name=gate_name, status="Not Started"))
        db.session.commit()
        log(request.form.get("owner", "system"), "PROJECT_CREATED", f"id={p.id} name={p.name}")
        flash(f"Project '{p.name}' created with 6 security gates initialized.")
        return redirect(url_for("projects"))
    all_projects = Project.query.all()
    compliance = {p.id: project_gate_compliance(p) for p in all_projects}
    return render_template(
        "projects.html", projects=all_projects, compliance=compliance,
        project_types=PROJECT_TYPES, criticalities=CRITICALITIES,
    )


@app.route("/projects/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    gates = sorted(project.gates, key=lambda g: GATE_NAMES.index(g.gate_name))
    return render_template(
        "project_detail.html", project=project, gates=gates,
        gate_statuses=GATE_STATUSES, compliance=project_gate_compliance(project),
    )


@app.route("/gates/<int:gate_id>/update", methods=["POST"])
def update_gate(gate_id):
    g = SecurityGate.query.get_or_404(gate_id)
    old_status = g.status
    g.status = request.form["status"]
    g.approver = request.form.get("approver", g.approver)
    g.gate_date = request.form.get("gate_date", g.gate_date)
    if request.form.get("evidence_notes"):
        g.evidence_notes = request.form["evidence_notes"]
    db.session.commit()
    log(g.approver or "system", "GATE_STATUS_CHANGED",
        f"project_id={g.project_id} gate={g.gate_name} {old_status} -> {g.status}")
    flash(f"Gate '{g.gate_name}' updated: {old_status} → {g.status}")
    return redirect(url_for("project_detail", project_id=g.project_id))


@app.route("/scripts", methods=["GET", "POST"])
def scripts():
    if request.method == "POST":
        s = ThirdPartyScript(
            name=request.form["name"], page_context=request.form["page_context"],
            source_url=request.form.get("source_url"), sri_pinned="sri_pinned" in request.form,
            last_reviewed=request.form.get("last_reviewed"), risk_level=request.form["risk_level"],
            notes=request.form.get("notes"),
        )
        db.session.add(s)
        db.session.commit()
        log("Project Security Owner", "SCRIPT_ADDED", f"id={s.id} name={s.name}")
        flash("Script added to register.")
        return redirect(url_for("scripts"))
    return render_template("scripts.html", scripts=ThirdPartyScript.query.all(), risk_levels=RISK_LEVELS)


@app.route("/scripts/<int:script_id>/update", methods=["POST"])
def update_script(script_id):
    s = ThirdPartyScript.query.get_or_404(script_id)
    old_pinned = s.sri_pinned
    s.sri_pinned = "sri_pinned" in request.form
    s.last_reviewed = request.form.get("last_reviewed", s.last_reviewed)
    s.notes = request.form.get("notes", s.notes)
    db.session.commit()
    log("Project Security Owner", "SCRIPT_UPDATED", f"{s.name}: SRI {old_pinned} -> {s.sri_pinned}")
    flash(f"Script '{s.name}' updated.")
    return redirect(url_for("scripts"))


@app.route("/changes", methods=["GET", "POST"])
def changes():
    if request.method == "POST":
        c = ChangeRecord(
            project_id=int(request.form["project_id"]) if request.form.get("project_id") else None,
            title=request.form["title"], change_type=request.form.get("change_type"),
            deployed_at=request.form.get("deployed_at"), gate_passed="gate_passed" in request.form,
            approver=request.form.get("approver"), notes=request.form.get("notes"),
        )
        db.session.add(c)
        db.session.commit()
        log(request.form.get("approver", "system"), "CHANGE_LOGGED", f"id={c.id} title={c.title}")
        flash("Change logged.")
        return redirect(url_for("changes"))
    return render_template("changes.html", changes=ChangeRecord.query.all(), projects=Project.query.all())


@app.route("/audit")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    projects_list = Project.query.all()
    scripts_list = ThirdPartyScript.query.all()
    changes_list = ChangeRecord.query.all()
    gates = SecurityGate.query.all()

    total_gates = len(gates)
    passed_gates = len([g for g in gates if g.status == "Passed"])
    overall_compliance = round((passed_gates / total_gates) * 100, 1) if total_gates else 0
    unprotected_scripts = [s for s in scripts_list if not s.sri_pinned]
    ungated_changes = [c for c in changes_list if not c.gate_passed]
    project_gates = {p.id: sorted(p.gates, key=lambda g: GATE_NAMES.index(g.gate_name)) for p in projects_list}

    return render_template(
        "report.html", projects=projects_list, scripts=scripts_list, changes=changes_list,
        overall_compliance=overall_compliance, unprotected_scripts=unprotected_scripts,
        ungated_changes=ungated_changes, project_gates=project_gates,
        compliance_fn=project_gate_compliance, generated_at=datetime.utcnow(),
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5007, debug=True)
