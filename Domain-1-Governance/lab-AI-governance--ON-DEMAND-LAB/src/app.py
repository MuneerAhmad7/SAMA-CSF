"""
AI Governance & Model Risk Evidence Tracker — Lab 10 (Air Canada chatbot scenario)

The central design problem this app solves: SAMA CSF / NCA ECC style controls assume
a deterministic yes/no answer ("is the patch applied", "is the policy published").
AI systems don't offer that — the same system can answer differently each time.
So instead of a binary control status, the core evidence mechanic here is a
*sampled, trended accuracy rate* (see OutputSample + sample_accuracy()), which is
what actually gets presented to a Board for a probabilistic system.

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aigovernance.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

SYSTEM_TYPES = ["Customer Chatbot", "Fraud/Anomaly Detection Model", "Credit Scoring Model",
                "Internal Developer Copilot", "Marketing Content Generator"]
RISK_TIERS = ["Critical", "High", "Medium", "Low"]
INCIDENT_SEVERITIES = ["Critical", "High", "Medium", "Low"]
INCIDENT_STATUSES = ["Open", "Investigating", "Resolved"]
CHANGE_TYPES = ["Model Version Upgrade", "Prompt Change", "Fine-Tuning", "Guardrail Update"]
CHANGE_STATUSES = ["Pending", "Approved", "Rejected"]


# ---------- Models ----------
class AISystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    system_type = db.Column(db.String(50))
    risk_tier = db.Column(db.String(20))
    owner = db.Column(db.String(100))
    model_version = db.Column(db.String(50))
    deployed_date = db.Column(db.String(20))
    description = db.Column(db.Text)

    checkpoints = db.relationship("OversightCheckpoint", backref="ai_system", lazy=True)
    samples = db.relationship("OutputSample", backref="ai_system", lazy=True)
    incidents = db.relationship("Incident", backref="ai_system", lazy=True)
    changes = db.relationship("ModelChange", backref="ai_system", lazy=True)


class OversightCheckpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ai_system_id = db.Column(db.Integer, db.ForeignKey("ai_system.id"))
    checkpoint_name = db.Column(db.String(150))
    trigger_condition = db.Column(db.String(300))
    enforced = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


class OutputSample(db.Model):
    """A periodic batch review — the core non-deterministic-evidence mechanic.
    You can't test every possible output, so you sample N real outputs, score them
    against a rubric, and track the rate over time."""
    id = db.Column(db.Integer, primary_key=True)
    ai_system_id = db.Column(db.Integer, db.ForeignKey("ai_system.id"))
    sample_date = db.Column(db.String(20))
    sample_size = db.Column(db.Integer)
    reviewer = db.Column(db.String(100))
    accurate_count = db.Column(db.Integer, default=0)
    inaccurate_count = db.Column(db.Integer, default=0)
    escalation_needed_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ai_system_id = db.Column(db.Integer, db.ForeignKey("ai_system.id"))
    incident_date = db.Column(db.String(20))
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))
    root_cause = db.Column(db.Text)
    remediation = db.Column(db.Text)
    status = db.Column(db.String(20), default="Open")


class ModelChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ai_system_id = db.Column(db.Integer, db.ForeignKey("ai_system.id"))
    change_date = db.Column(db.String(20))
    change_type = db.Column(db.String(30))
    description = db.Column(db.Text)
    approver = db.Column(db.String(100))
    status = db.Column(db.String(20), default="Pending")


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


def sample_accuracy(samples):
    """Weighted accuracy rate across a set of sample batches — the headline
    'evidence number' for a non-deterministic system."""
    total = sum(s.sample_size or 0 for s in samples)
    accurate = sum(s.accurate_count or 0 for s in samples)
    if total == 0:
        return None
    return round((accurate / total) * 100, 1)


def escalation_rate(samples):
    total = sum(s.sample_size or 0 for s in samples)
    escalations = sum(s.escalation_needed_count or 0 for s in samples)
    if total == 0:
        return None
    return round((escalations / total) * 100, 1)


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    systems = AISystem.query.all()
    all_samples = OutputSample.query.all()
    incidents = Incident.query.all()
    changes = ModelChange.query.all()
    checkpoints = OversightCheckpoint.query.all()

    overall_accuracy = sample_accuracy(all_samples)
    overall_escalation = escalation_rate(all_samples)
    open_incidents = [i for i in incidents if i.status != "Resolved"]
    pending_changes = [c for c in changes if c.status == "Pending"]
    unenforced_checkpoints = [c for c in checkpoints if not c.enforced]

    system_accuracy = []
    for s in systems:
        acc = sample_accuracy(s.samples)
        system_accuracy.append({"system": s, "accuracy": acc, "sample_count": sum(x.sample_size or 0 for x in s.samples)})

    risk_counts = {t: len([s for s in systems if s.risk_tier == t]) for t in RISK_TIERS}

    return render_template(
        "dashboard.html", system_count=len(systems), overall_accuracy=overall_accuracy,
        overall_escalation=overall_escalation, open_incidents=open_incidents,
        pending_changes=pending_changes, unenforced_checkpoints=unenforced_checkpoints,
        system_accuracy=system_accuracy, risk_counts=risk_counts,
    )


@app.route("/systems", methods=["GET", "POST"])
def systems():
    if request.method == "POST":
        s = AISystem(
            name=request.form["name"], system_type=request.form["system_type"],
            risk_tier=request.form["risk_tier"], owner=request.form.get("owner"),
            model_version=request.form.get("model_version"), deployed_date=request.form.get("deployed_date"),
            description=request.form.get("description"),
        )
        db.session.add(s)
        db.session.commit()
        log(request.form.get("owner", "system"), "AI_SYSTEM_ADDED", f"id={s.id} name={s.name}")
        flash("AI system added.")
        return redirect(url_for("systems"))
    all_systems = AISystem.query.all()
    accuracy_map = {s.id: sample_accuracy(s.samples) for s in all_systems}
    return render_template(
        "systems.html", systems=all_systems, accuracy_map=accuracy_map,
        system_types=SYSTEM_TYPES, risk_tiers=RISK_TIERS,
    )


@app.route("/systems/<int:system_id>")
def system_detail(system_id):
    s = AISystem.query.get_or_404(system_id)
    accuracy = sample_accuracy(s.samples)
    escalation = escalation_rate(s.samples)
    return render_template("system_detail.html", system=s, accuracy=accuracy, escalation=escalation)


@app.route("/checkpoints", methods=["GET", "POST"])
def checkpoints():
    if request.method == "POST":
        c = OversightCheckpoint(
            ai_system_id=int(request.form["ai_system_id"]), checkpoint_name=request.form["checkpoint_name"],
            trigger_condition=request.form.get("trigger_condition"), enforced="enforced" in request.form,
            notes=request.form.get("notes"),
        )
        db.session.add(c)
        db.session.commit()
        log("AI Governance Owner", "CHECKPOINT_ADDED", f"id={c.id} name={c.checkpoint_name}")
        flash("Checkpoint added.")
        return redirect(url_for("checkpoints"))
    return render_template("checkpoints.html", checkpoints=OversightCheckpoint.query.all(),
                            systems=AISystem.query.all())


@app.route("/checkpoints/<int:checkpoint_id>/update", methods=["POST"])
def update_checkpoint(checkpoint_id):
    c = OversightCheckpoint.query.get_or_404(checkpoint_id)
    old_enforced = c.enforced
    c.enforced = "enforced" in request.form
    c.notes = request.form.get("notes", c.notes)
    db.session.commit()
    log("AI Governance Owner", "CHECKPOINT_UPDATED", f"{c.checkpoint_name}: enforced {old_enforced} -> {c.enforced}")
    flash(f"Checkpoint '{c.checkpoint_name}' updated.")
    return redirect(url_for("checkpoints"))


@app.route("/samples", methods=["GET", "POST"])
def samples():
    if request.method == "POST":
        s = OutputSample(
            ai_system_id=int(request.form["ai_system_id"]), sample_date=request.form.get("sample_date"),
            sample_size=int(request.form["sample_size"]), reviewer=request.form.get("reviewer"),
            accurate_count=int(request.form.get("accurate_count") or 0),
            inaccurate_count=int(request.form.get("inaccurate_count") or 0),
            escalation_needed_count=int(request.form.get("escalation_needed_count") or 0),
            notes=request.form.get("notes"),
        )
        db.session.add(s)
        db.session.commit()
        log(request.form.get("reviewer", "system"), "SAMPLE_REVIEW_LOGGED",
            f"id={s.id} system_id={s.ai_system_id} size={s.sample_size}")
        flash("Sample review logged.")
        return redirect(url_for("samples"))
    all_samples = OutputSample.query.order_by(OutputSample.sample_date.desc()).all()
    return render_template("samples.html", samples=all_samples, systems=AISystem.query.all())


@app.route("/incidents", methods=["GET", "POST"])
def incidents():
    if request.method == "POST":
        i = Incident(
            ai_system_id=int(request.form["ai_system_id"]), incident_date=request.form.get("incident_date"),
            description=request.form.get("description"), severity=request.form["severity"],
            root_cause=request.form.get("root_cause"), remediation=request.form.get("remediation"),
            status="Open",
        )
        db.session.add(i)
        db.session.commit()
        log("AI Governance Owner", "INCIDENT_LOGGED", f"id={i.id} system_id={i.ai_system_id}")
        flash("Incident logged.")
        return redirect(url_for("incidents"))
    return render_template("incidents.html", incidents=Incident.query.all(), systems=AISystem.query.all(),
                            severities=INCIDENT_SEVERITIES)


@app.route("/incidents/<int:incident_id>/update", methods=["POST"])
def update_incident(incident_id):
    i = Incident.query.get_or_404(incident_id)
    old_status = i.status
    i.status = request.form["status"]
    if request.form.get("remediation"):
        i.remediation = request.form["remediation"]
    db.session.commit()
    log("AI Governance Owner", "INCIDENT_STATUS_CHANGED", f"id={i.id} {old_status} -> {i.status}")
    flash(f"Incident updated: {old_status} → {i.status}")
    return redirect(url_for("incidents"))


@app.route("/changes", methods=["GET", "POST"])
def changes():
    if request.method == "POST":
        c = ModelChange(
            ai_system_id=int(request.form["ai_system_id"]), change_date=request.form.get("change_date"),
            change_type=request.form["change_type"], description=request.form.get("description"),
            status="Pending",
        )
        db.session.add(c)
        db.session.commit()
        log("AI Governance Owner", "MODEL_CHANGE_LOGGED", f"id={c.id} system_id={c.ai_system_id}")
        flash("Model change logged.")
        return redirect(url_for("changes"))
    return render_template("changes.html", changes=ModelChange.query.all(), systems=AISystem.query.all(),
                            change_types=CHANGE_TYPES)


@app.route("/changes/<int:change_id>/update", methods=["POST"])
def update_change(change_id):
    c = ModelChange.query.get_or_404(change_id)
    old_status = c.status
    c.status = request.form["status"]
    c.approver = request.form.get("approver", c.approver)
    db.session.commit()
    log(c.approver or "system", "MODEL_CHANGE_STATUS_CHANGED", f"id={c.id} {old_status} -> {c.status}")
    flash(f"Model change updated: {old_status} → {c.status}")
    return redirect(url_for("changes"))


@app.route("/audit")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    systems_list = AISystem.query.all()
    all_samples = OutputSample.query.all()
    incidents_list = Incident.query.all()
    changes_list = ModelChange.query.all()
    checkpoints_list = OversightCheckpoint.query.all()

    overall_accuracy = sample_accuracy(all_samples)
    overall_escalation = escalation_rate(all_samples)
    open_incidents = [i for i in incidents_list if i.status != "Resolved"]
    unenforced = [c for c in checkpoints_list if not c.enforced]

    system_accuracy = {s.id: sample_accuracy(s.samples) for s in systems_list}

    return render_template(
        "report.html", systems=systems_list, samples=all_samples, incidents=incidents_list,
        changes=changes_list, checkpoints=checkpoints_list, overall_accuracy=overall_accuracy,
        overall_escalation=overall_escalation, open_incidents=open_incidents, unenforced=unenforced,
        system_accuracy=system_accuracy, generated_at=datetime.utcnow(),
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5009, debug=True)
