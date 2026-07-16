"""
Cyber Security Audit & Assurance Tracker — Lab 11 (SolarWinds 2020 scenario)

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

import sla

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///audit.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

ENGAGEMENT_TYPES = ["Internal Audit", "External Audit", "Penetration Test", "Regulatory Examination"]
ENGAGEMENT_STATUSES = ["Planned", "In Progress", "Completed", "Report Issued"]
SEVERITIES = ["Critical", "High", "Medium", "Low"]
FINDING_STATUSES = ["Open", "In Progress", "Remediated", "Verified Closed"]


# ---------- Models ----------
class AuditEngagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    engagement_type = db.Column(db.String(30))
    scope = db.Column(db.String(300))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    auditor = db.Column(db.String(150))
    status = db.Column(db.String(20), default="Planned")

    findings = db.relationship("Finding", backref="engagement", lazy=True)


class Finding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    engagement_id = db.Column(db.Integer, db.ForeignKey("audit_engagement.id"))
    title = db.Column(db.String(200))
    category = db.Column(db.String(100))
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    owner = db.Column(db.String(100))
    identified_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Open")
    root_cause = db.Column(db.Text)
    is_repeat = db.Column(db.Boolean, default=False)
    repeat_notes = db.Column(db.String(300))
    closed_at = db.Column(db.DateTime, nullable=True)


class CommitteeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_date = db.Column(db.String(20))
    summary = db.Column(db.Text)
    overdue_highlighted = db.Column(db.Text)
    attendees = db.Column(db.String(300))


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


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    now = datetime.utcnow()
    findings = Finding.query.all()
    engagements = AuditEngagement.query.all()

    total = len(findings)
    open_findings = [f for f in findings if f.status not in sla.CLOSED_STATUSES]
    overdue = [f for f in open_findings if sla.is_overdue(f, now)]
    compliant_pct = round(((total - len(overdue)) / total) * 100, 1) if total else 100.0

    repeat_findings = [f for f in findings if f.is_repeat]
    severity_counts = {s: len([f for f in findings if f.severity == s]) for s in SEVERITIES}
    overdue_sorted = sorted(overdue, key=lambda f: sla.days_overdue(f, now), reverse=True)

    upcoming = [e for e in engagements if e.status in ("Planned", "In Progress")]

    return render_template(
        "dashboard.html", total=total, open_count=len(open_findings), overdue=overdue_sorted,
        overdue_count=len(overdue), compliant_pct=compliant_pct, severity_counts=severity_counts,
        repeat_findings=repeat_findings, engagement_count=len(engagements), upcoming=upcoming,
        now=now, sla=sla,
    )


@app.route("/engagements", methods=["GET", "POST"])
def engagements():
    if request.method == "POST":
        e = AuditEngagement(
            name=request.form["name"], engagement_type=request.form["engagement_type"],
            scope=request.form.get("scope"), start_date=request.form.get("start_date"),
            end_date=request.form.get("end_date"), auditor=request.form.get("auditor"),
            status="Planned",
        )
        db.session.add(e)
        db.session.commit()
        log(request.form.get("auditor", "system"), "ENGAGEMENT_CREATED", f"id={e.id} name={e.name}")
        flash("Engagement added.")
        return redirect(url_for("engagements"))
    all_engagements = AuditEngagement.query.all()
    finding_counts = {e.id: len(e.findings) for e in all_engagements}
    return render_template(
        "engagements.html", engagements=all_engagements, finding_counts=finding_counts,
        engagement_types=ENGAGEMENT_TYPES, statuses=ENGAGEMENT_STATUSES,
    )


@app.route("/engagements/<int:engagement_id>/update", methods=["POST"])
def update_engagement(engagement_id):
    e = AuditEngagement.query.get_or_404(engagement_id)
    old_status = e.status
    e.status = request.form["status"]
    db.session.commit()
    log("Audit Owner", "ENGAGEMENT_STATUS_CHANGED", f"id={e.id} {old_status} -> {e.status}")
    flash(f"Engagement updated: {old_status} → {e.status}")
    return redirect(url_for("engagements"))


@app.route("/findings", methods=["GET", "POST"])
def findings():
    if request.method == "POST":
        f = Finding(
            engagement_id=int(request.form["engagement_id"]), title=request.form["title"],
            category=request.form.get("category"), severity=request.form["severity"],
            description=request.form.get("description"), recommendation=request.form.get("recommendation"),
            owner=request.form.get("owner"), identified_at=datetime.utcnow(), status="Open",
            root_cause=request.form.get("root_cause"), is_repeat="is_repeat" in request.form,
            repeat_notes=request.form.get("repeat_notes"),
        )
        db.session.add(f)
        db.session.commit()
        log(request.form.get("owner", "system"), "FINDING_CREATED", f"id={f.id} title={f.title}")
        flash("Finding logged.")
        return redirect(url_for("findings"))

    now = datetime.utcnow()
    all_findings = Finding.query.order_by(Finding.identified_at.desc()).all()
    all_engagements = AuditEngagement.query.all()

    severity_filter = request.args.get("severity")
    status_filter = request.args.get("status")
    if severity_filter:
        all_findings = [f for f in all_findings if f.severity == severity_filter]
    if status_filter:
        all_findings = [f for f in all_findings if f.status == status_filter]

    return render_template(
        "findings.html", findings=all_findings, engagements=all_engagements, now=now, sla=sla,
        statuses=FINDING_STATUSES, severities=SEVERITIES,
        severity_filter=severity_filter, status_filter=status_filter,
    )


@app.route("/findings/<int:finding_id>/update", methods=["POST"])
def update_finding(finding_id):
    f = Finding.query.get_or_404(finding_id)
    old_status = f.status
    f.status = request.form["status"]
    f.owner = request.form.get("owner", f.owner)
    note = request.form.get("note", "")
    if note:
        f.root_cause = (f.root_cause + "\n" if f.root_cause else "") + f"[Update] {note}"
    if f.status in sla.CLOSED_STATUSES and not f.closed_at:
        f.closed_at = datetime.utcnow()
    if f.status not in sla.CLOSED_STATUSES:
        f.closed_at = None
    db.session.commit()
    log(f.owner or "system", "FINDING_STATUS_CHANGED", f"id={f.id} {old_status} -> {f.status}")
    flash(f"Finding '{f.title}' updated: {old_status} → {f.status}")
    return redirect(url_for("findings"))


@app.route("/committee", methods=["GET", "POST"])
def committee():
    if request.method == "POST":
        r = CommitteeReport(
            meeting_date=request.form.get("meeting_date"), summary=request.form.get("summary"),
            overdue_highlighted=request.form.get("overdue_highlighted"), attendees=request.form.get("attendees"),
        )
        db.session.add(r)
        db.session.commit()
        log("Audit Owner", "COMMITTEE_REPORT_LOGGED", f"id={r.id} date={r.meeting_date}")
        flash("Committee report logged.")
        return redirect(url_for("committee"))
    return render_template("committee.html", reports=CommitteeReport.query.all())


@app.route("/audit-log")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    now = datetime.utcnow()
    findings_list = Finding.query.order_by(Finding.severity).all()
    engagements_list = AuditEngagement.query.all()
    committee_reports = CommitteeReport.query.all()

    total = len(findings_list)
    open_findings = [f for f in findings_list if f.status not in sla.CLOSED_STATUSES]
    overdue = [f for f in open_findings if sla.is_overdue(f, now)]
    compliant_pct = round(((total - len(overdue)) / total) * 100, 1) if total else 100.0
    repeat_findings = [f for f in findings_list if f.is_repeat]
    severity_counts = {s: len([f for f in findings_list if f.severity == s]) for s in SEVERITIES}

    return render_template(
        "report.html", findings=findings_list, engagements=engagements_list, committee_reports=committee_reports,
        total=total, overdue=overdue, compliant_pct=compliant_pct, repeat_findings=repeat_findings,
        severity_counts=severity_counts, now=now, sla=sla, generated_at=now,
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5010, debug=True)
