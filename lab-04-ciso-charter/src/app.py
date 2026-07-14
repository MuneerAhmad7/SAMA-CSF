"""
CISO Charter Builder & Authority Assessment — Lab 04 (Target 2013 scenario)

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cisocharter.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

# Ordered charter sections: key -> (label, help text, is_textarea)
CHARTER_FIELDS = [
    ("organization_name", "Organization Name", "Legal/operating name of the organization", False),
    ("ciso_name", "CISO Name", "Currently appointed CISO", False),
    ("reports_to", "CISO Reports To", "e.g. CEO / Board Risk & Compliance Committee", False),
    ("mandate_statement", "Mandate Statement",
     "1-2 sentences: what authority and scope does the CISO hold?", True),
    ("independence_statement", "Independence from IT",
     "How is the cybersecurity function organizationally separated from IT operations?", True),
    ("budget_authority", "Budget Authority",
     "What spending can the CISO approve independently, and up to what threshold?", False),
    ("escalation_authority", "Direct Escalation Authority",
     "Can the CISO escalate directly to the Board/CEO without IT sign-off? Describe the path.", True),
    ("committee_name", "Cyber Security Committee",
     "Name and mandate of the oversight committee the CISO chairs or reports into", False),
    ("committee_frequency", "Committee Meeting Frequency", "e.g. Quarterly minimum", False),
    ("term_review_cycle", "Charter Review Cycle", "e.g. Annual, or upon major organizational change", False),
    ("board_reporting_frequency", "Board Reporting Frequency", "e.g. Quarterly", False),
    ("scope_statement", "Scope of Authority",
     "Which business units, systems, and third parties fall under this Charter?", True),
]

# Authority & independence assessment controls — modeled directly on the Target 2013 gaps
AUTHORITY_CONTROLS = [
    ("AUTH-1", "CISO is organizationally independent from IT (does not report through the CIO/IT Director)"),
    ("AUTH-2", "CISO has a direct, documented reporting line to the CEO or Board Risk Committee"),
    ("AUTH-3", "CISO can escalate a security event directly to the Board/CEO without requiring IT approval"),
    ("AUTH-4", "CISO has independent budget authority up to a defined threshold"),
    ("AUTH-5", "CISO has authority to mandate security requirements across all business units"),
    ("AUTH-6", "CISO chairs or has a formal seat on a Board-level Cyber Security Committee"),
    ("AUTH-7", "Charter defines who has authority to declare a security incident 'critical' and mobilize response"),
    ("AUTH-8", "Security alerts from monitoring tools have a documented, time-bound escalation path to a named accountable owner"),
    ("AUTH-9", "CISO performance objectives are set and reviewed independently of IT leadership"),
    ("AUTH-10", "CISO has authority to halt or delay a business/IT project on security grounds, subject to documented override process"),
    ("AUTH-11", "Charter is formally approved by the Board, not just signed off by IT management"),
    ("AUTH-12", "Charter is reviewed at least annually or after any major security incident"),
    ("AUTH-13", "Third-party/vendor risk decisions above a defined threshold require CISO sign-off"),
    ("AUTH-14", "CISO role/authority does not depend on a single individual — succession/continuity plan documented"),
]

STATUS_OPTIONS = ["Not Implemented", "Partial", "Implemented"]


# ---------- Models ----------
class CharterField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)


class AuthorityControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(300))
    status = db.Column(db.String(20), default="Not Implemented")
    evidence = db.Column(db.String(300))


class RaciEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(200), nullable=False)
    responsible = db.Column(db.String(120))
    accountable = db.Column(db.String(120))
    consulted = db.Column(db.String(120))
    informed = db.Column(db.String(120))


class EscalationRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    severity = db.Column(db.String(30))
    trigger = db.Column(db.String(200))
    escalate_to = db.Column(db.String(150))
    timeframe = db.Column(db.String(50))


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    actor = db.Column(db.String(100))
    action = db.Column(db.String(80))
    details = db.Column(db.String(400))


def log(actor, action, details=""):
    db.session.add(AuditLog(actor=actor, action=action, details=details))
    db.session.commit()


def get_charter_dict():
    fields = {f.field_key: f.value for f in CharterField.query.all()}
    return fields


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    charter = get_charter_dict()
    filled = sum(1 for k, *_ in CHARTER_FIELDS if charter.get(k))
    total_fields = len(CHARTER_FIELDS)
    completeness_pct = round((filled / total_fields) * 100, 1) if total_fields else 0

    controls = AuthorityControl.query.all()
    total_controls = len(controls)
    implemented = len([c for c in controls if c.status == "Implemented"])
    partial = len([c for c in controls if c.status == "Partial"])
    authority_pct = round(((implemented + 0.5 * partial) / total_controls) * 100, 1) if total_controls else 0

    gaps = [c for c in controls if c.status != "Implemented"]

    return render_template(
        "dashboard.html", completeness_pct=completeness_pct, filled=filled, total_fields=total_fields,
        authority_pct=authority_pct, implemented=implemented, total_controls=total_controls,
        gaps=gaps, raci_count=RaciEntry.query.count(), escalation_count=EscalationRule.query.count(),
        ciso_name=charter.get("ciso_name", "—"), org_name=charter.get("organization_name", "—"),
    )


@app.route("/charter", methods=["GET", "POST"])
def charter():
    if request.method == "POST":
        for key, *_ in CHARTER_FIELDS:
            value = request.form.get(key, "")
            field = CharterField.query.filter_by(field_key=key).first()
            if field:
                field.value = value
            else:
                field = CharterField(field_key=key, value=value)
                db.session.add(field)
        db.session.commit()
        log("CISO", "CHARTER_UPDATED", "Charter fields saved")
        flash("Charter saved.")
        return redirect(url_for("charter"))

    charter_data = get_charter_dict()
    return render_template("charter.html", fields=CHARTER_FIELDS, data=charter_data)


@app.route("/authority", methods=["GET", "POST"])
def authority():
    if request.method == "POST":
        control = AuthorityControl.query.get(request.form["control_id"])
        control.status = request.form["status"]
        control.evidence = request.form["evidence"]
        db.session.commit()
        log("CISO", "AUTHORITY_CONTROL_UPDATED", f"{control.control_id} -> {control.status}")
        flash("Control updated.")
        return redirect(url_for("authority"))
    return render_template("authority.html", controls=AuthorityControl.query.all())


@app.route("/raci", methods=["GET", "POST"])
def raci():
    if request.method == "POST":
        r = RaciEntry(
            activity=request.form["activity"], responsible=request.form["responsible"],
            accountable=request.form["accountable"], consulted=request.form["consulted"],
            informed=request.form["informed"],
        )
        db.session.add(r)
        db.session.commit()
        log("CISO", "RACI_ADDED", request.form["activity"])
        flash("RACI entry added.")
        return redirect(url_for("raci"))
    return render_template("raci.html", entries=RaciEntry.query.all())


@app.route("/escalation", methods=["GET", "POST"])
def escalation():
    if request.method == "POST":
        e = EscalationRule(
            severity=request.form["severity"], trigger=request.form["trigger"],
            escalate_to=request.form["escalate_to"], timeframe=request.form["timeframe"],
        )
        db.session.add(e)
        db.session.commit()
        log("CISO", "ESCALATION_RULE_ADDED", request.form["trigger"])
        flash("Escalation rule added.")
        return redirect(url_for("escalation"))
    return render_template("escalation.html", rules=EscalationRule.query.all())


@app.route("/audit")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    charter_data = get_charter_dict()
    controls = AuthorityControl.query.all()
    raci_entries = RaciEntry.query.all()
    escalation_rules = EscalationRule.query.all()

    implemented = len([c for c in controls if c.status == "Implemented"])
    partial = len([c for c in controls if c.status == "Partial"])
    total_controls = len(controls)
    authority_pct = round(((implemented + 0.5 * partial) / total_controls) * 100, 1) if total_controls else 0

    return render_template(
        "report.html", data=charter_data, fields=CHARTER_FIELDS, controls=controls,
        raci_entries=raci_entries, escalation_rules=escalation_rules,
        authority_pct=authority_pct, generated_at=datetime.utcnow(),
    )


def init_db():
    db.create_all()
    if AuthorityControl.query.count() == 0:
        for cid, desc in AUTHORITY_CONTROLS:
            db.session.add(AuthorityControl(control_id=cid, description=desc))
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5003, debug=True)
