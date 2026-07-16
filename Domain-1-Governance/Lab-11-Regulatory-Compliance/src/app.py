"""
Regulatory Compliance & Multi-Framework Obligations Tracker — Lab 12 (Uber 2016/2017 scenario)

Core mechanic: one incident can trigger multiple, independent regulatory notification
clocks at once (SAMA CSF, PDPL, PCI-DSS, ...), each with its own deadline. This app
computes each clock's status live rather than relying on a manually-tracked checklist.

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///regcompliance.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

REGULATORS = ["SAMA", "NCA", "SDAIA", "PCI Security Standards Council", "SWIFT"]
INCIDENT_SEVERITIES = ["Critical", "High", "Medium", "Low"]
GAP_SEVERITIES = ["Critical", "High", "Medium", "Low"]
GAP_STATUSES = ["Open", "In Progress", "Remediated", "Verified Closed"]
GAP_CLOSED = {"Remediated", "Verified Closed"}
CORRESPONDENCE_TYPES = ["Examination Request", "Breach Notification", "Formal Inquiry", "Response", "Routine Filing"]
CORRESPONDENCE_STATUSES = ["Open", "Responded", "Closed"]


# ---------- Models ----------
class RegulatoryFramework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    regulator = db.Column(db.String(60))
    critical_notification_deadline_hours = db.Column(db.Float)
    scope_description = db.Column(db.Text)
    owner = db.Column(db.String(100))

    notifications = db.relationship("NotificationRequirement", backref="framework", lazy=True)
    gaps = db.relationship("ComplianceGap", backref="framework", lazy=True)
    correspondence = db.relationship("RegulatoryCorrespondence", backref="framework", lazy=True)


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
    affected_data_types = db.Column(db.String(300))

    notifications = db.relationship("NotificationRequirement", backref="incident", lazy=True)


class NotificationRequirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    framework_id = db.Column(db.Integer, db.ForeignKey("regulatory_framework.id"))
    deadline_hours = db.Column(db.Float)
    notified_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)


class ComplianceGap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    framework_id = db.Column(db.Integer, db.ForeignKey("regulatory_framework.id"))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))
    owner = db.Column(db.String(100))
    identified_at = db.Column(db.String(20))
    due_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Open")
    cross_reference = db.Column(db.String(200))


class RegulatoryCorrespondence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    framework_id = db.Column(db.Integer, db.ForeignKey("regulatory_framework.id"))
    regulator = db.Column(db.String(60))
    correspondence_type = db.Column(db.String(40))
    date = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    status = db.Column(db.String(20), default="Open")
    due_date = db.Column(db.String(20))
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


# ---------- Core notification-clock logic ----------
def notification_deadline(req):
    return req.incident.discovered_at + timedelta(hours=req.deadline_hours)


def notification_status(req, now):
    """Returns (status_label, css_class, hours_value)."""
    deadline = notification_deadline(req)
    if req.notified_at:
        delta_hours = (req.notified_at - deadline).total_seconds() / 3600
        if req.notified_at <= deadline:
            return "Notified On Time", "notif-ontime", round((deadline - req.notified_at).total_seconds() / 3600, 1)
        return "Notified LATE", "notif-late", round(delta_hours, 1)
    else:
        if now > deadline:
            overdue_hours = (now - deadline).total_seconds() / 3600
            return "PENDING — OVERDUE", "notif-overdue", round(overdue_hours, 1)
        remaining_hours = (deadline - now).total_seconds() / 3600
        return "Pending — Within Window", "notif-pending", round(remaining_hours, 1)


def format_hours(h):
    """Human-friendly hours-to-days formatting for large values."""
    if h is None:
        return "—"
    if abs(h) >= 48:
        return f"{round(h / 24, 1)}d"
    return f"{h}h"


def on_time_rate(requirements):
    notified = [r for r in requirements if r.notified_at]
    if not notified:
        return None
    on_time = [r for r in notified if r.notified_at <= notification_deadline(r)]
    return round((len(on_time) / len(notified)) * 100, 1)


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    now = datetime.utcnow()
    frameworks = RegulatoryFramework.query.all()
    all_requirements = NotificationRequirement.query.all()
    gaps = ComplianceGap.query.all()
    correspondence = RegulatoryCorrespondence.query.all()

    rate = on_time_rate(all_requirements)
    overdue_pending = [r for r in all_requirements if notification_status(r, now)[1] == "notif-overdue"]
    late_notified = [r for r in all_requirements if notification_status(r, now)[1] == "notif-late"]
    open_gaps = [g for g in gaps if g.status not in GAP_CLOSED]
    overdue_correspondence = [c for c in correspondence if c.status != "Closed" and c.due_date and c.due_date < now.strftime("%Y-%m-%d")]

    gap_by_framework = {}
    for fw in frameworks:
        gap_by_framework[fw.id] = len([g for g in fw.gaps if g.status not in GAP_CLOSED])

    return render_template(
        "dashboard.html", framework_count=len(frameworks), on_time_rate=rate,
        overdue_pending=overdue_pending, late_notified=late_notified, open_gaps=open_gaps,
        overdue_correspondence=overdue_correspondence, gap_by_framework=gap_by_framework,
        frameworks=frameworks, now=now, notification_status=notification_status, format_hours=format_hours,
    )


@app.route("/frameworks", methods=["GET", "POST"])
def frameworks():
    if request.method == "POST":
        fw = RegulatoryFramework(
            name=request.form["name"], regulator=request.form["regulator"],
            critical_notification_deadline_hours=float(request.form["deadline_hours"]),
            scope_description=request.form.get("scope_description"), owner=request.form.get("owner"),
        )
        db.session.add(fw)
        db.session.commit()
        log(request.form.get("owner", "system"), "FRAMEWORK_ADDED", f"id={fw.id} name={fw.name}")
        flash("Regulatory framework added.")
        return redirect(url_for("frameworks"))
    return render_template("frameworks.html", frameworks=RegulatoryFramework.query.all(), regulators=REGULATORS)


@app.route("/incidents", methods=["GET", "POST"])
def incidents():
    if request.method == "POST":
        discovered_str = request.form.get("discovered_at")
        discovered_at = datetime.strptime(discovered_str, "%Y-%m-%dT%H:%M") if discovered_str else datetime.utcnow()
        inc = Incident(
            title=request.form["title"], discovered_at=discovered_at, severity=request.form["severity"],
            description=request.form.get("description"), affected_data_types=request.form.get("affected_data_types"),
        )
        db.session.add(inc)
        db.session.commit()

        framework_ids = request.form.getlist("framework_ids")
        for fid in framework_ids:
            fw = RegulatoryFramework.query.get(int(fid))
            db.session.add(NotificationRequirement(
                incident_id=inc.id, framework_id=fw.id,
                deadline_hours=fw.critical_notification_deadline_hours,
            ))
        db.session.commit()
        log("Compliance Owner", "INCIDENT_LOGGED", f"id={inc.id} title={inc.title} frameworks={len(framework_ids)}")
        flash(f"Incident logged with {len(framework_ids)} notification requirement(s) created.")
        return redirect(url_for("notifications"))
    return render_template("incidents.html", incidents=Incident.query.all(),
                            frameworks=RegulatoryFramework.query.all(), severities=INCIDENT_SEVERITIES)


@app.route("/notifications")
def notifications():
    now = datetime.utcnow()
    all_requirements = NotificationRequirement.query.all()
    incidents_list = Incident.query.order_by(Incident.discovered_at.desc()).all()
    return render_template(
        "notifications.html", incidents=incidents_list, now=now,
        notification_status=notification_status, notification_deadline=notification_deadline,
        format_hours=format_hours,
    )


@app.route("/notifications/<int:req_id>/notify", methods=["POST"])
def mark_notified(req_id):
    r = NotificationRequirement.query.get_or_404(req_id)
    notified_str = request.form.get("notified_at")
    r.notified_at = datetime.strptime(notified_str, "%Y-%m-%dT%H:%M") if notified_str else datetime.utcnow()
    r.notes = request.form.get("notes", r.notes)
    db.session.commit()
    status_label, _, _ = notification_status(r, datetime.utcnow())
    log("Compliance Owner", "NOTIFICATION_RECORDED",
        f"req_id={r.id} framework={r.framework.name} incident={r.incident.title} status={status_label}")
    flash(f"Notification recorded: {status_label}")
    return redirect(url_for("notifications"))


@app.route("/gaps", methods=["GET", "POST"])
def gaps():
    if request.method == "POST":
        g = ComplianceGap(
            framework_id=int(request.form["framework_id"]), title=request.form["title"],
            description=request.form.get("description"), severity=request.form["severity"],
            owner=request.form.get("owner"), identified_at=request.form.get("identified_at"),
            due_date=request.form.get("due_date"), status="Open",
            cross_reference=request.form.get("cross_reference"),
        )
        db.session.add(g)
        db.session.commit()
        log(request.form.get("owner", "system"), "GAP_CREATED", f"id={g.id} title={g.title}")
        flash("Compliance gap logged.")
        return redirect(url_for("gaps"))
    return render_template("gaps.html", gaps=ComplianceGap.query.all(), frameworks=RegulatoryFramework.query.all(),
                            severities=GAP_SEVERITIES, statuses=GAP_STATUSES)


@app.route("/gaps/<int:gap_id>/update", methods=["POST"])
def update_gap(gap_id):
    g = ComplianceGap.query.get_or_404(gap_id)
    old_status = g.status
    g.status = request.form["status"]
    db.session.commit()
    log("Compliance Owner", "GAP_STATUS_CHANGED", f"id={g.id} {old_status} -> {g.status}")
    flash(f"Gap updated: {old_status} → {g.status}")
    return redirect(url_for("gaps"))


@app.route("/correspondence", methods=["GET", "POST"])
def correspondence():
    if request.method == "POST":
        c = RegulatoryCorrespondence(
            framework_id=int(request.form["framework_id"]), regulator=request.form["regulator"],
            correspondence_type=request.form["correspondence_type"], date=request.form.get("date"),
            subject=request.form["subject"], status="Open", due_date=request.form.get("due_date"),
            notes=request.form.get("notes"),
        )
        db.session.add(c)
        db.session.commit()
        log("Compliance Owner", "CORRESPONDENCE_LOGGED", f"id={c.id} subject={c.subject}")
        flash("Correspondence logged.")
        return redirect(url_for("correspondence"))
    return render_template("correspondence.html", correspondence=RegulatoryCorrespondence.query.all(),
                            frameworks=RegulatoryFramework.query.all(), regulators=REGULATORS,
                            types=CORRESPONDENCE_TYPES, statuses=CORRESPONDENCE_STATUSES,
                            today=datetime.utcnow().strftime("%Y-%m-%d"))


@app.route("/correspondence/<int:corr_id>/update", methods=["POST"])
def update_correspondence(corr_id):
    c = RegulatoryCorrespondence.query.get_or_404(corr_id)
    old_status = c.status
    c.status = request.form["status"]
    db.session.commit()
    log("Compliance Owner", "CORRESPONDENCE_STATUS_CHANGED", f"id={c.id} {old_status} -> {c.status}")
    flash(f"Correspondence updated: {old_status} → {c.status}")
    return redirect(url_for("correspondence"))


@app.route("/audit-log")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    now = datetime.utcnow()
    frameworks_list = RegulatoryFramework.query.all()
    incidents_list = Incident.query.order_by(Incident.discovered_at.desc()).all()
    all_requirements = NotificationRequirement.query.all()
    gaps_list = ComplianceGap.query.all()
    correspondence_list = RegulatoryCorrespondence.query.all()

    rate = on_time_rate(all_requirements)
    open_gaps = [g for g in gaps_list if g.status not in GAP_CLOSED]
    late_or_overdue = [r for r in all_requirements if notification_status(r, now)[1] in ("notif-late", "notif-overdue")]

    return render_template(
        "report.html", frameworks=frameworks_list, incidents=incidents_list, gaps=gaps_list,
        correspondence=correspondence_list, on_time_rate=rate, open_gaps=open_gaps,
        late_or_overdue=late_or_overdue, now=now, notification_status=notification_status,
        notification_deadline=notification_deadline, format_hours=format_hours, generated_at=now,
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5011, debug=True)
