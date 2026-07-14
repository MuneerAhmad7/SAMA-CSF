"""
Cybersecurity Strategy Builder & Maturity Roadmap — Lab 05 (Sony Pictures 2014 scenario)

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///strategy.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

STRATEGY_FIELDS = [
    ("organization_name", "Organization Name", "Legal/operating name", False),
    ("vision_statement", "Vision Statement", "What does 'secure' look like for this organization in 3-5 years?", True),
    ("strategic_period", "Strategic Period", "e.g. 2026-2029", False),
    ("business_alignment", "Business Alignment",
     "How does this strategy support the organization's business objectives?", True),
    ("threat_landscape_summary", "Threat Landscape Summary",
     "Top external/internal threats considered when setting this strategy", True),
    ("total_budget", "Total Multi-Year Budget (SAR)", "", False),
    ("review_cycle", "Review Cycle", "e.g. Annual, or upon major incident/threat shift", False),
    ("approved_by", "Approved By", "e.g. Board Risk & Compliance Committee", False),
    ("approval_date", "Approval Date", "", False),
]

MATURITY_DOMAINS = [
    "Governance & Leadership", "Risk Management", "Identity & Access Management",
    "Network & Infrastructure Security", "Application Security", "Data Protection",
    "Incident Response", "Third-Party & Cloud Security", "Business Continuity",
    "Security Awareness & Training",
]

PHASES = ["Foundation", "Core Controls", "Advanced Controls", "Optimization"]
INITIATIVE_STATUSES = ["Not Started", "In Progress", "Delayed", "Completed"]
LIKELIHOOD_IMPACT = ["Low", "Medium", "High"]


# ---------- Models ----------
class StrategyField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)


class MaturityScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(80), unique=True)
    current_level = db.Column(db.Integer, default=0)
    target_level = db.Column(db.Integer, default=3)
    notes = db.Column(db.String(300))


class ThreatItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threat_type = db.Column(db.String(100))
    description = db.Column(db.String(300))
    likelihood = db.Column(db.String(20))
    impact = db.Column(db.String(20))
    relevance_notes = db.Column(db.String(300))


class Initiative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    phase = db.Column(db.String(30))
    domain = db.Column(db.String(80))
    owner = db.Column(db.String(100))
    budget_allocated = db.Column(db.Float, default=0)
    budget_spent = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="Not Started")
    target_quarter = db.Column(db.String(20))


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    actor = db.Column(db.String(100))
    action = db.Column(db.String(80))
    details = db.Column(db.String(400))


def log(actor, action, details=""):
    db.session.add(AuditLog(actor=actor, action=action, details=details))
    db.session.commit()


def get_strategy_dict():
    return {f.field_key: f.value for f in StrategyField.query.all()}


def risk_score(likelihood, impact):
    scale = {"Low": 1, "Medium": 2, "High": 3}
    return scale.get(likelihood, 1) * scale.get(impact, 1)


def init_db():
    db.create_all()
    if MaturityScore.query.count() == 0:
        for d in MATURITY_DOMAINS:
            db.session.add(MaturityScore(domain=d, current_level=0, target_level=3))
        db.session.commit()


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    strategy = get_strategy_dict()
    filled = sum(1 for k, *_ in STRATEGY_FIELDS if strategy.get(k))
    completeness_pct = round((filled / len(STRATEGY_FIELDS)) * 100, 1) if STRATEGY_FIELDS else 0

    scores = MaturityScore.query.all()
    avg_current = round(sum(s.current_level for s in scores) / len(scores), 1) if scores else 0
    avg_target = round(sum(s.target_level for s in scores) / len(scores), 1) if scores else 0
    widest_gaps = sorted(scores, key=lambda s: (s.target_level - s.current_level), reverse=True)[:3]

    initiatives = Initiative.query.all()
    total_initiatives = len(initiatives)
    completed = len([i for i in initiatives if i.status == "Completed"])
    delayed = len([i for i in initiatives if i.status == "Delayed"])
    completion_pct = round((completed / total_initiatives) * 100, 1) if total_initiatives else 0

    total_allocated = sum(i.budget_allocated or 0 for i in initiatives)
    total_spent = sum(i.budget_spent or 0 for i in initiatives)
    budget_utilization = round((total_spent / total_allocated) * 100, 1) if total_allocated else 0

    threats = ThreatItem.query.all()
    high_risk_threats = [t for t in threats if risk_score(t.likelihood, t.impact) >= 6]

    phase_progress = {}
    for phase in PHASES:
        phase_initiatives = [i for i in initiatives if i.phase == phase]
        phase_completed = len([i for i in phase_initiatives if i.status == "Completed"])
        phase_progress[phase] = {
            "total": len(phase_initiatives),
            "completed": phase_completed,
            "pct": round((phase_completed / len(phase_initiatives)) * 100, 1) if phase_initiatives else 0,
        }

    return render_template(
        "dashboard.html", completeness_pct=completeness_pct, avg_current=avg_current, avg_target=avg_target,
        widest_gaps=widest_gaps, total_initiatives=total_initiatives, completed=completed, delayed=delayed,
        completion_pct=completion_pct, total_allocated=total_allocated, total_spent=total_spent,
        budget_utilization=budget_utilization, high_risk_threats=high_risk_threats, phase_progress=phase_progress,
        org_name=strategy.get("organization_name", "—"), phases=PHASES,
    )


@app.route("/strategy", methods=["GET", "POST"])
def strategy():
    if request.method == "POST":
        for key, *_ in STRATEGY_FIELDS:
            value = request.form.get(key, "")
            field = StrategyField.query.filter_by(field_key=key).first()
            if field:
                field.value = value
            else:
                db.session.add(StrategyField(field_key=key, value=value))
        db.session.commit()
        log("Strategy Owner", "STRATEGY_UPDATED", "Strategy fields saved")
        flash("Strategy saved.")
        return redirect(url_for("strategy"))
    return render_template("strategy.html", fields=STRATEGY_FIELDS, data=get_strategy_dict())


@app.route("/maturity", methods=["GET", "POST"])
def maturity():
    if request.method == "POST":
        score = MaturityScore.query.get(request.form["score_id"])
        score.current_level = int(request.form["current_level"])
        score.target_level = int(request.form["target_level"])
        score.notes = request.form.get("notes", "")
        db.session.commit()
        log("Strategy Owner", "MATURITY_UPDATED", f"{score.domain}: current={score.current_level} target={score.target_level}")
        flash("Maturity score updated.")
        return redirect(url_for("maturity"))
    scores = MaturityScore.query.all()
    return render_template("maturity.html", scores=scores)


@app.route("/threats", methods=["GET", "POST"])
def threats():
    if request.method == "POST":
        t = ThreatItem(
            threat_type=request.form["threat_type"], description=request.form["description"],
            likelihood=request.form["likelihood"], impact=request.form["impact"],
            relevance_notes=request.form.get("relevance_notes", ""),
        )
        db.session.add(t)
        db.session.commit()
        log("Strategy Owner", "THREAT_ADDED", request.form["threat_type"])
        flash("Threat added.")
        return redirect(url_for("threats"))
    all_threats = ThreatItem.query.all()
    return render_template("threats.html", threats=all_threats, risk_score=risk_score)


@app.route("/roadmap", methods=["GET", "POST"])
def roadmap():
    if request.method == "POST":
        i = Initiative(
            title=request.form["title"], phase=request.form["phase"], domain=request.form["domain"],
            owner=request.form["owner"], budget_allocated=float(request.form.get("budget_allocated") or 0),
            budget_spent=float(request.form.get("budget_spent") or 0), status=request.form["status"],
            target_quarter=request.form.get("target_quarter", ""),
        )
        db.session.add(i)
        db.session.commit()
        log("Strategy Owner", "INITIATIVE_ADDED", request.form["title"])
        flash("Initiative added.")
        return redirect(url_for("roadmap"))
    initiatives = Initiative.query.all()
    return render_template("roadmap.html", initiatives=initiatives, phases=PHASES,
                            domains=MATURITY_DOMAINS, statuses=INITIATIVE_STATUSES)


@app.route("/roadmap/<int:initiative_id>/update", methods=["POST"])
def update_initiative(initiative_id):
    i = Initiative.query.get_or_404(initiative_id)
    i.status = request.form["status"]
    i.budget_spent = float(request.form.get("budget_spent") or i.budget_spent or 0)
    db.session.commit()
    log("Strategy Owner", "INITIATIVE_UPDATED", f"{i.title} -> {i.status}, spent={i.budget_spent}")
    flash(f"Initiative '{i.title}' updated.")
    return redirect(url_for("roadmap"))


@app.route("/audit")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    strategy_data = get_strategy_dict()
    scores = MaturityScore.query.all()
    threats_list = ThreatItem.query.all()
    initiatives = Initiative.query.order_by(Initiative.phase).all()

    total_allocated = sum(i.budget_allocated or 0 for i in initiatives)
    total_spent = sum(i.budget_spent or 0 for i in initiatives)

    return render_template(
        "report.html", data=strategy_data, fields=STRATEGY_FIELDS, scores=scores, threats=threats_list,
        initiatives=initiatives, phases=PHASES, risk_score=risk_score,
        total_allocated=total_allocated, total_spent=total_spent, generated_at=datetime.utcnow(),
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5004, debug=True)
