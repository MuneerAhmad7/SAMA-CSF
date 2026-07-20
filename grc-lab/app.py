import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

from models import db, GRCItem, Policy, Acknowledgment, Incident
from seed import seed_if_empty

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DATA_DIR, 'grc.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("SECRET_KEY", "grc-lab-dev-secret")

db.init_app(app)

CATEGORIES = ["Governance", "Risk Management", "Compliance"]
STATUSES = ["Not Started", "In Progress", "Implemented", "Reviewed", "Approved"]
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
INCIDENT_STATUSES = ["Open", "Investigating", "Contained", "Resolved"]


with app.app_context():
    db.create_all()
    seed_if_empty()


# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    items = GRCItem.query.all()
    total = len(items) or 1

    by_category = {c: len([i for i in items if i.category == c]) for c in CATEGORIES}
    by_status = {s: len([i for i in items if i.status == s]) for s in STATUSES}
    by_risk = {r: len([i for i in items if i.risk_level == r]) for r in RISK_LEVELS}

    open_high_critical = len([
        i for i in items
        if i.risk_level in ("High", "Critical") and i.status in ("Not Started", "In Progress")
    ])

    policies = Policy.query.all()
    incidents = Incident.query.order_by(Incident.reported_at.desc()).all()
    open_incidents = len([i for i in incidents if i.status != "Resolved"])

    return render_template(
        "dashboard.html",
        total=len(items),
        by_category=by_category,
        by_status=by_status,
        by_risk=by_risk,
        total_for_pct=total,
        open_high_critical=open_high_critical,
        policy_count=len(policies),
        incident_count=len(incidents),
        open_incidents=open_incidents,
    )


# ---------------------------------------------------------------------
# GRC Register (Governance / Risk / Compliance items)
# ---------------------------------------------------------------------
@app.route("/grc")
def grc_list():
    query = GRCItem.query

    category = request.args.get("category", "")
    status = request.args.get("status", "")
    risk = request.args.get("risk", "")
    search = request.args.get("q", "")

    if category:
        query = query.filter(GRCItem.category == category)
    if status:
        query = query.filter(GRCItem.status == status)
    if risk:
        query = query.filter(GRCItem.risk_level == risk)
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(GRCItem.grc_item.ilike(like), GRCItem.owner.ilike(like))
        )

    items = query.order_by(GRCItem.category, GRCItem.subcategory).all()

    return render_template(
        "grc_list.html",
        items=items,
        categories=CATEGORIES,
        statuses=STATUSES,
        risks=RISK_LEVELS,
        selected_category=category,
        selected_status=status,
        selected_risk=risk,
        search=search,
    )


@app.route("/grc/new", methods=["GET", "POST"])
def grc_new():
    if request.method == "POST":
        item = GRCItem(**_grc_form_to_dict(request.form))
        db.session.add(item)
        db.session.commit()
        flash(f"GRC item '{item.grc_item}' created.", "success")
        return redirect(url_for("grc_detail", item_id=item.id))

    return render_template(
        "grc_form.html", item=None, categories=CATEGORIES,
        statuses=STATUSES, risks=RISK_LEVELS,
    )


@app.route("/grc/<int:item_id>")
def grc_detail(item_id):
    item = GRCItem.query.get_or_404(item_id)
    return render_template("grc_detail.html", item=item)


@app.route("/grc/<int:item_id>/edit", methods=["GET", "POST"])
def grc_edit(item_id):
    item = GRCItem.query.get_or_404(item_id)

    if request.method == "POST":
        for key, value in _grc_form_to_dict(request.form).items():
            setattr(item, key, value)
        db.session.commit()
        flash(f"GRC item '{item.grc_item}' updated.", "success")
        return redirect(url_for("grc_detail", item_id=item.id))

    return render_template(
        "grc_form.html", item=item, categories=CATEGORIES,
        statuses=STATUSES, risks=RISK_LEVELS,
    )


@app.route("/grc/<int:item_id>/delete", methods=["POST"])
def grc_delete(item_id):
    item = GRCItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f"GRC item '{item.grc_item}' deleted.", "info")
    return redirect(url_for("grc_list"))


def _grc_form_to_dict(form):
    return dict(
        category=form.get("category", "").strip(),
        subcategory=form.get("subcategory", "").strip(),
        grc_item=form.get("grc_item", "").strip(),
        description=form.get("description", "").strip(),
        objective=form.get("objective", "").strip(),
        owner=form.get("owner", "").strip(),
        status=form.get("status", "Not Started"),
        due_date=form.get("due_date", "").strip(),
        implementation_steps=form.get("implementation_steps", "").strip(),
        testing_method=form.get("testing_method", "").strip(),
        risk_level=form.get("risk_level", "Medium"),
        mitigation_strategy=form.get("mitigation_strategy", "").strip(),
        compliance_standard=form.get("compliance_standard", "").strip(),
        mock_data_example=form.get("mock_data_example", "").strip(),
        notes=form.get("notes", "").strip(),
    )


# ---------------------------------------------------------------------
# Policy Management (Governance policy in action: acknowledgment tracking)
# ---------------------------------------------------------------------
@app.route("/policies")
def policies():
    all_policies = Policy.query.all()
    return render_template("policies.html", policies=all_policies)


@app.route("/policies/new", methods=["GET", "POST"])
def policy_new():
    if request.method == "POST":
        policy = Policy(
            name=request.form.get("name", "").strip(),
            category=request.form.get("category", "").strip(),
            description=request.form.get("description", "").strip(),
            version=request.form.get("version", "1.0").strip(),
            effective_date=request.form.get("effective_date", "").strip(),
        )
        db.session.add(policy)
        db.session.commit()
        flash(f"Policy '{policy.name}' created.", "success")
        return redirect(url_for("policies"))

    return render_template("policy_form.html", categories=CATEGORIES)


@app.route("/policies/<int:policy_id>/acknowledge", methods=["POST"])
def policy_acknowledge(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    employee_name = request.form.get("employee_name", "").strip()

    if not employee_name:
        flash("Please enter an employee name to acknowledge the policy.", "error")
        return redirect(url_for("policies"))

    already = Acknowledgment.query.filter_by(
        policy_id=policy.id, employee_name=employee_name
    ).first()
    if already:
        flash(f"{employee_name} has already acknowledged '{policy.name}'.", "info")
    else:
        db.session.add(Acknowledgment(policy_id=policy.id, employee_name=employee_name))
        db.session.commit()
        flash(f"{employee_name} acknowledged '{policy.name}'.", "success")

    return redirect(url_for("policies"))


# ---------------------------------------------------------------------
# Incident Response (Risk Management control in action)
# ---------------------------------------------------------------------
@app.route("/incidents")
def incidents():
    all_incidents = Incident.query.order_by(Incident.reported_at.desc()).all()
    return render_template(
        "incidents.html", incidents=all_incidents, statuses=INCIDENT_STATUSES
    )


@app.route("/incidents/new", methods=["GET", "POST"])
def incident_new():
    if request.method == "POST":
        incident = Incident(
            title=request.form.get("title", "").strip(),
            description=request.form.get("description", "").strip(),
            severity=request.form.get("severity", "Medium"),
            status="Open",
            reported_by=request.form.get("reported_by", "").strip(),
            reported_at=datetime.utcnow(),
        )
        db.session.add(incident)
        db.session.commit()
        flash(f"Incident '{incident.title}' logged.", "success")
        return redirect(url_for("incidents"))

    return render_template("incident_form.html", risks=RISK_LEVELS)


@app.route("/incidents/<int:incident_id>/status", methods=["POST"])
def incident_update_status(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    new_status = request.form.get("status", incident.status)
    incident.status = new_status
    if new_status == "Resolved" and incident.resolved_at is None:
        incident.resolved_at = datetime.utcnow()
    if new_status != "Resolved":
        incident.resolved_at = None
    db.session.commit()
    flash(f"Incident '{incident.title}' marked as {new_status}.", "success")
    return redirect(url_for("incidents"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
