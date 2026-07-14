"""
Policy Framework Manager — Lab 06 (Marriott/Starwood 2018 scenario)

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///policyframework.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

POLICY_TYPES = ["Master Policy", "Domain Policy", "Standard", "Procedure", "Guideline"]
POLICY_STATUSES = ["Draft", "Review", "Approved", "Published", "Retired"]

CONTROL_DOMAINS = [
    "Governance", "Identity & Access Management", "Data Protection", "Cryptography",
    "Incident Response", "Business Continuity", "Third-Party & M&A Security",
    "Human Resources Security", "Physical Security", "Cloud Security", "Security Awareness & Training",
]

ENTITY_TYPES = ["Wholly-Owned Subsidiary", "Recent Acquisition", "Third-Party Partner"]


# ---------- Models ----------
class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    policy_type = db.Column(db.String(30), default="Domain Policy")
    domain = db.Column(db.String(80))
    owner = db.Column(db.String(100))
    status = db.Column(db.String(20), default="Draft")
    version = db.Column(db.String(10), default="0.1")
    effective_date = db.Column(db.String(20))
    review_date = db.Column(db.String(20))
    parent_id = db.Column(db.Integer, db.ForeignKey("policy.id"), nullable=True)
    notes = db.Column(db.Text)

    children = db.relationship("Policy", backref=db.backref("parent", remote_side=[id]))


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    entity_type = db.Column(db.String(30))
    acquired_or_onboarded_date = db.Column(db.String(20))
    integration_pct = db.Column(db.Integer, default=0)
    gap_notes = db.Column(db.Text)


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


def is_overdue(review_date_str, today_str):
    if not review_date_str:
        return False
    try:
        return review_date_str < today_str
    except Exception:
        return False


def build_tree(policies):
    """Build nested tree structure from flat policy list using parent_id."""
    by_id = {p.id: {"policy": p, "children": []} for p in policies}
    roots = []
    for p in policies:
        node = by_id[p.id]
        if p.parent_id and p.parent_id in by_id:
            by_id[p.parent_id]["children"].append(node)
        else:
            roots.append(node)
    return roots


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    policies = Policy.query.all()
    total = len(policies)
    published = len([p for p in policies if p.status == "Published"])
    overdue_reviews = [p for p in policies if p.status == "Published" and is_overdue(p.review_date, today)]

    covered_domains = {p.domain for p in policies if p.status in ("Approved", "Published") and p.domain}
    gap_domains = [d for d in CONTROL_DOMAINS if d not in covered_domains]
    coverage_pct = round((len(CONTROL_DOMAINS) - len(gap_domains)) / len(CONTROL_DOMAINS) * 100, 1) if CONTROL_DOMAINS else 0

    entities = Entity.query.all()
    avg_integration = round(sum(e.integration_pct for e in entities) / len(entities), 1) if entities else 0
    at_risk_entities = [e for e in entities if e.integration_pct < 70]

    return render_template(
        "dashboard.html", total=total, published=published, overdue_reviews=overdue_reviews,
        coverage_pct=coverage_pct, gap_domains=gap_domains, avg_integration=avg_integration,
        at_risk_entities=at_risk_entities, entity_count=len(entities),
    )


@app.route("/policies", methods=["GET", "POST"])
def policies():
    if request.method == "POST":
        parent_id = request.form.get("parent_id")
        p = Policy(
            title=request.form["title"], policy_type=request.form["policy_type"],
            domain=request.form.get("domain") or None, owner=request.form.get("owner"),
            status="Draft", version=request.form.get("version", "0.1"),
            effective_date=request.form.get("effective_date"), review_date=request.form.get("review_date"),
            parent_id=int(parent_id) if parent_id else None, notes=request.form.get("notes"),
        )
        db.session.add(p)
        db.session.commit()
        log(request.form.get("owner", "system"), "POLICY_CREATED", f"id={p.id} title={p.title}")
        flash("Policy added.")
        return redirect(url_for("policies"))

    today = datetime.utcnow().strftime("%Y-%m-%d")
    all_policies = Policy.query.order_by(Policy.policy_type).all()
    return render_template(
        "policies.html", policies=all_policies, today=today,
        policy_types=POLICY_TYPES, statuses=POLICY_STATUSES, domains=CONTROL_DOMAINS,
        possible_parents=Policy.query.all(),
    )


@app.route("/policies/<int:policy_id>/update", methods=["POST"])
def update_policy(policy_id):
    p = Policy.query.get_or_404(policy_id)
    old_status = p.status
    p.status = request.form["status"]
    p.version = request.form.get("version", p.version)
    if request.form.get("review_date"):
        p.review_date = request.form["review_date"]
    db.session.commit()
    log(request.form.get("owner", "system"), "POLICY_STATUS_CHANGED",
        f"id={p.id} title={p.title} {old_status} -> {p.status}")
    flash(f"Policy '{p.title}' updated: {old_status} → {p.status}")
    return redirect(url_for("policies"))


@app.route("/hierarchy")
def hierarchy():
    policies = Policy.query.all()
    tree = build_tree(policies)
    return render_template("hierarchy.html", tree=tree)


@app.route("/coverage")
def coverage():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    policies = Policy.query.all()
    coverage_map = {}
    for d in CONTROL_DOMAINS:
        matching = [p for p in policies if p.domain == d]
        active = [p for p in matching if p.status in ("Approved", "Published")]
        coverage_map[d] = {
            "policies": matching,
            "covered": len(active) > 0,
            "overdue": any(is_overdue(p.review_date, today) for p in active),
        }
    return render_template("coverage.html", coverage_map=coverage_map)


@app.route("/entities", methods=["GET", "POST"])
def entities():
    if request.method == "POST":
        e = Entity(
            name=request.form["name"], entity_type=request.form["entity_type"],
            acquired_or_onboarded_date=request.form.get("acquired_or_onboarded_date"),
            integration_pct=int(request.form.get("integration_pct") or 0),
            gap_notes=request.form.get("gap_notes"),
        )
        db.session.add(e)
        db.session.commit()
        log("Policy Owner", "ENTITY_ADDED", f"id={e.id} name={e.name}")
        flash("Entity added.")
        return redirect(url_for("entities"))
    return render_template("entities.html", entities=Entity.query.all(), entity_types=ENTITY_TYPES)


@app.route("/entities/<int:entity_id>/update", methods=["POST"])
def update_entity(entity_id):
    e = Entity.query.get_or_404(entity_id)
    old_pct = e.integration_pct
    e.integration_pct = int(request.form.get("integration_pct") or e.integration_pct)
    e.gap_notes = request.form.get("gap_notes", e.gap_notes)
    db.session.commit()
    log("Policy Owner", "ENTITY_INTEGRATION_UPDATED",
        f"{e.name}: {old_pct}% -> {e.integration_pct}%")
    flash(f"Entity '{e.name}' updated.")
    return redirect(url_for("entities"))


@app.route("/audit")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    policies = Policy.query.order_by(Policy.policy_type).all()
    tree = build_tree(policies)
    entities_list = Entity.query.all()

    covered_domains = {p.domain for p in policies if p.status in ("Approved", "Published") and p.domain}
    gap_domains = [d for d in CONTROL_DOMAINS if d not in covered_domains]
    coverage_pct = round((len(CONTROL_DOMAINS) - len(gap_domains)) / len(CONTROL_DOMAINS) * 100, 1) if CONTROL_DOMAINS else 0
    overdue_reviews = [p for p in policies if p.status == "Published" and is_overdue(p.review_date, today)]

    return render_template(
        "report.html", policies=policies, tree=tree, entities=entities_list, domains=CONTROL_DOMAINS,
        covered_domains=covered_domains, gap_domains=gap_domains, coverage_pct=coverage_pct,
        overdue_reviews=overdue_reviews, generated_at=datetime.utcnow(),
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5005, debug=True)
