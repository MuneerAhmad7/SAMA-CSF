"""
Cloud Security Posture Manager — Lab 07 (Capital One 2019 scenario)

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cspm.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

RESOURCE_TYPES = ["S3 Bucket", "IAM Role", "Security Group", "WAF ACL", "RDS Instance", "EC2 Instance"]
ENVIRONMENTS = ["Production", "Staging", "Development"]
SEVERITIES = ["Critical", "High", "Medium", "Low"]
FINDING_STATUSES = ["Open", "Investigating", "Remediated", "Verified"]
CLOSED_STATUSES = {"Remediated", "Verified"}

# CSPM rule catalog — modeled on real cloud misconfiguration patterns
CSPM_RULES = [
    ("CSPM-01", "S3 Bucket Publicly Accessible", "High"),
    ("CSPM-02", "S3 Bucket Missing Encryption at Rest", "Medium"),
    ("CSPM-03", "S3 Bucket Missing Access Logging", "Medium"),
    ("CSPM-04", "IAM Role with Wildcard (*:*) Permissions", "Critical"),
    ("CSPM-05", "IAM Role Attached to Public-Facing Resource with Excessive S3 Access", "Critical"),
    ("CSPM-06", "Security Group Open to 0.0.0.0/0 on Sensitive Port", "High"),
    ("CSPM-07", "WAF Not Enabled or Misconfigured on Public-Facing Application", "Critical"),
    ("CSPM-08", "MFA Not Enforced on IAM/Root User", "High"),
    ("CSPM-09", "Unencrypted Storage Volume (EBS/RDS)", "Medium"),
    ("CSPM-10", "No Continuous Cloud Security Posture Monitoring in Place", "High"),
]


# ---------- Models ----------
class CloudResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    resource_type = db.Column(db.String(30))
    environment = db.Column(db.String(20))
    owner = db.Column(db.String(100))
    sensitivity = db.Column(db.String(20))
    identifier = db.Column(db.String(150))

    findings = db.relationship("Finding", backref="resource", lazy=True)


class Finding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.String(20))
    title = db.Column(db.String(200))
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
    resource_id = db.Column(db.Integer, db.ForeignKey("cloud_resource.id"))
    status = db.Column(db.String(20), default="Open")
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.Column(db.String(100))
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


def posture_score(findings):
    """Weighted posture score: 100 minus penalty per open finding by severity."""
    weights = {"Critical": 10, "High": 5, "Medium": 3, "Low": 1}
    open_findings = [f for f in findings if f.status not in CLOSED_STATUSES]
    penalty = sum(weights.get(f.severity, 1) for f in open_findings)
    return max(0, round(100 - penalty, 1))


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    findings = Finding.query.all()
    resources = CloudResource.query.all()

    score = posture_score(findings)
    open_findings = [f for f in findings if f.status not in CLOSED_STATUSES]
    critical_open = [f for f in open_findings if f.severity == "Critical"]
    severity_counts = {s: len([f for f in findings if f.severity == s]) for s in SEVERITIES}
    open_by_severity = {s: len([f for f in open_findings if f.severity == s]) for s in SEVERITIES}

    prod_resources = [r for r in resources if r.environment == "Production"]
    prod_findings = [f for f in open_findings if f.resource and f.resource.environment == "Production"]

    return render_template(
        "dashboard.html", score=score, total_findings=len(findings), open_count=len(open_findings),
        critical_open=critical_open, severity_counts=severity_counts, open_by_severity=open_by_severity,
        resource_count=len(resources), prod_resource_count=len(prod_resources),
        prod_findings_count=len(prod_findings),
    )


@app.route("/resources", methods=["GET", "POST"])
def resources():
    if request.method == "POST":
        r = CloudResource(
            name=request.form["name"], resource_type=request.form["resource_type"],
            environment=request.form["environment"], owner=request.form.get("owner"),
            sensitivity=request.form["sensitivity"], identifier=request.form.get("identifier"),
        )
        db.session.add(r)
        db.session.commit()
        log(request.form.get("owner", "system"), "RESOURCE_ADDED", f"id={r.id} name={r.name}")
        flash("Resource added.")
        return redirect(url_for("resources"))
    all_resources = CloudResource.query.all()
    finding_counts = {r.id: len([f for f in r.findings if f.status not in CLOSED_STATUSES]) for r in all_resources}
    return render_template(
        "resources.html", resources=all_resources, finding_counts=finding_counts,
        resource_types=RESOURCE_TYPES, environments=ENVIRONMENTS, severities=SEVERITIES,
    )


@app.route("/findings", methods=["GET", "POST"])
def findings():
    if request.method == "POST":
        f = Finding(
            rule_id=request.form["rule_id"], title=request.form["title"], severity=request.form["severity"],
            description=request.form.get("description"), resource_id=int(request.form["resource_id"]),
            status="Open", owner=request.form.get("owner"),
        )
        db.session.add(f)
        db.session.commit()
        log(request.form.get("owner", "system"), "FINDING_CREATED", f"id={f.id} rule={f.rule_id}")
        flash("Finding logged.")
        return redirect(url_for("findings"))

    all_findings = Finding.query.order_by(Finding.discovered_at.desc()).all()
    all_resources = CloudResource.query.all()

    severity_filter = request.args.get("severity")
    status_filter = request.args.get("status")
    if severity_filter:
        all_findings = [f for f in all_findings if f.severity == severity_filter]
    if status_filter:
        all_findings = [f for f in all_findings if f.status == status_filter]

    return render_template(
        "findings.html", findings=all_findings, resources=all_resources, rules=CSPM_RULES,
        severities=SEVERITIES, statuses=FINDING_STATUSES,
        severity_filter=severity_filter, status_filter=status_filter,
    )


@app.route("/findings/<int:finding_id>/update", methods=["POST"])
def update_finding(finding_id):
    f = Finding.query.get_or_404(finding_id)
    old_status = f.status
    f.status = request.form["status"]
    f.owner = request.form.get("owner", f.owner)
    note = request.form.get("notes", "")
    if note:
        f.notes = (f.notes + "\n" if f.notes else "") + note
    db.session.commit()
    log(f.owner or "system", "FINDING_STATUS_CHANGED",
        f"id={f.id} {old_status} -> {f.status}" + (f" note={note}" if note else ""))
    flash(f"Finding '{f.title}' updated: {old_status} → {f.status}")
    return redirect(url_for("findings"))


@app.route("/audit")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    findings_list = Finding.query.order_by(Finding.severity).all()
    resources_list = CloudResource.query.all()
    score = posture_score(findings_list)
    severity_counts = {s: len([f for f in findings_list if f.severity == s]) for s in SEVERITIES}
    open_findings = [f for f in findings_list if f.status not in CLOSED_STATUSES]

    return render_template(
        "report.html", findings=findings_list, resources=resources_list, score=score,
        severity_counts=severity_counts, open_findings=open_findings, rules=CSPM_RULES,
        generated_at=datetime.utcnow(),
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5006, debug=True)
