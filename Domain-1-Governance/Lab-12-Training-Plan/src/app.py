"""
Security Team Training & Certification Plan Tracker — Lab 13 (OPM 2015 scenario)

Distinct from Lab 09 (org-wide awareness): this app tracks the security TEAM's
technical depth specifically — skills matrix (current vs required competency),
certification expiry, and a funded, dated training plan tied to named gaps.

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trainingplan.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

ROLES = ["CISO", "SOC Analyst", "Security Engineer", "GRC Analyst", "Penetration Tester", "Incident Responder"]
SPECIALTIES = ["Incident Response", "Cloud Security", "Digital Forensics", "Penetration Testing",
               "GRC / Audit", "Secure Code Review"]
LEVELS = {0: "None", 1: "Novice", 2: "Basic", 3: "Proficient", 4: "Expert"}
PLAN_TYPES = ["Certification Prep", "Conference", "Formal Course", "Workshop", "Mentorship"]
PLAN_STATUSES = ["Planned", "In Progress", "Completed", "Delayed"]
PLAN_CLOSED = {"Completed"}


# ---------- Models ----------
class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(60))
    hire_date = db.Column(db.String(20))

    skill_assessments = db.relationship("SkillAssessment", backref="member", lazy=True)
    certifications = db.relationship("Certification", backref="member", lazy=True)
    plan_items = db.relationship("TrainingPlanItem", backref="member", lazy=True)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    category = db.Column(db.String(80))

    assessments = db.relationship("SkillAssessment", backref="skill", lazy=True)


class SkillAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("team_member.id"))
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"))
    current_level = db.Column(db.Integer, default=0)
    required_level = db.Column(db.Integer, default=2)
    assessed_date = db.Column(db.String(20))
    notes = db.Column(db.String(300))


class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("team_member.id"))
    name = db.Column(db.String(100))
    issuer = db.Column(db.String(100))
    issued_date = db.Column(db.String(20))
    expiry_date = db.Column(db.String(20))
    required_for_role = db.Column(db.Boolean, default=False)


class TrainingPlanItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("team_member.id"))
    title = db.Column(db.String(200))
    plan_type = db.Column(db.String(30))
    target_skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), nullable=True)
    budget = db.Column(db.Float, default=0)
    target_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Planned")
    notes = db.Column(db.Text)

    target_skill = db.relationship("Skill", foreign_keys=[target_skill_id])


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
    if Skill.query.count() == 0:
        for name in SPECIALTIES:
            db.session.add(Skill(name=name, category=name))
        db.session.commit()


def cert_status(cert, today_str):
    if not cert.expiry_date:
        return "Unknown", "cert-unknown"
    if cert.expiry_date < today_str:
        return "Expired", "cert-expired"
    warn_date = (datetime.strptime(cert.expiry_date, "%Y-%m-%d") - timedelta(days=90)).strftime("%Y-%m-%d")
    if today_str >= warn_date:
        return "Expiring Soon", "cert-expiring"
    return "Active", "cert-active"


# ---------- Routes ----------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    members = TeamMember.query.all()
    assessments = SkillAssessment.query.all()
    certs = Certification.query.all()
    plan_items = TrainingPlanItem.query.all()

    gaps = [(a, a.required_level - a.current_level) for a in assessments]
    widest_gaps = sorted(gaps, key=lambda x: x[1], reverse=True)[:5]
    widest_gaps = [g for g in widest_gaps if g[1] > 0]

    expired_certs = [c for c in certs if cert_status(c, today)[0] == "Expired"]
    expiring_certs = [c for c in certs if cert_status(c, today)[0] == "Expiring Soon"]

    total_plan = len(plan_items)
    completed_plan = len([p for p in plan_items if p.status == "Completed"])
    plan_completion_pct = round((completed_plan / total_plan) * 100, 1) if total_plan else 0
    delayed_plan = [p for p in plan_items if p.status == "Delayed"]

    total_budget = sum(p.budget or 0 for p in plan_items)

    return render_template(
        "dashboard.html", member_count=len(members), widest_gaps=widest_gaps,
        expired_certs=expired_certs, expiring_certs=expiring_certs,
        plan_completion_pct=plan_completion_pct, total_plan=total_plan, completed_plan=completed_plan,
        delayed_plan=delayed_plan, total_budget=total_budget, cert_status=cert_status, today=today,
        levels=LEVELS,
    )


@app.route("/team", methods=["GET", "POST"])
def team():
    if request.method == "POST":
        m = TeamMember(name=request.form["name"], role=request.form["role"], hire_date=request.form.get("hire_date"))
        db.session.add(m)
        db.session.commit()
        log("Training Plan Owner", "MEMBER_ADDED", f"id={m.id} name={m.name}")
        flash("Team member added.")
        return redirect(url_for("team"))
    return render_template("team.html", members=TeamMember.query.all(), roles=ROLES)


@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == "POST":
        existing = SkillAssessment.query.filter_by(
            member_id=int(request.form["member_id"]), skill_id=int(request.form["skill_id"])
        ).first()
        if existing:
            existing.current_level = int(request.form["current_level"])
            existing.required_level = int(request.form["required_level"])
            existing.assessed_date = request.form.get("assessed_date")
            existing.notes = request.form.get("notes")
        else:
            db.session.add(SkillAssessment(
                member_id=int(request.form["member_id"]), skill_id=int(request.form["skill_id"]),
                current_level=int(request.form["current_level"]), required_level=int(request.form["required_level"]),
                assessed_date=request.form.get("assessed_date"), notes=request.form.get("notes"),
            ))
        db.session.commit()
        log("Training Plan Owner", "SKILL_ASSESSED", f"member_id={request.form['member_id']} skill_id={request.form['skill_id']}")
        flash("Skill assessment saved.")
        return redirect(url_for("skills"))

    members = TeamMember.query.all()
    all_skills = Skill.query.all()
    matrix = {}
    for m in members:
        matrix[m.id] = {}
        for s in all_skills:
            a = SkillAssessment.query.filter_by(member_id=m.id, skill_id=s.id).first()
            matrix[m.id][s.id] = a
    return render_template("skills.html", members=members, skill_list=all_skills, matrix=matrix, levels=LEVELS)


@app.route("/certifications", methods=["GET", "POST"])
def certifications():
    if request.method == "POST":
        c = Certification(
            member_id=int(request.form["member_id"]), name=request.form["name"],
            issuer=request.form.get("issuer"), issued_date=request.form.get("issued_date"),
            expiry_date=request.form.get("expiry_date"), required_for_role="required_for_role" in request.form,
        )
        db.session.add(c)
        db.session.commit()
        log("Training Plan Owner", "CERTIFICATION_ADDED", f"id={c.id} name={c.name}")
        flash("Certification added.")
        return redirect(url_for("certifications"))
    today = datetime.utcnow().strftime("%Y-%m-%d")
    return render_template("certifications.html", certifications=Certification.query.all(),
                            members=TeamMember.query.all(), cert_status=cert_status, today=today)


@app.route("/plan", methods=["GET", "POST"])
def plan():
    if request.method == "POST":
        p = TrainingPlanItem(
            member_id=int(request.form["member_id"]), title=request.form["title"],
            plan_type=request.form["plan_type"],
            target_skill_id=int(request.form["target_skill_id"]) if request.form.get("target_skill_id") else None,
            budget=float(request.form.get("budget") or 0), target_date=request.form.get("target_date"),
            status="Planned", notes=request.form.get("notes"),
        )
        db.session.add(p)
        db.session.commit()
        log("Training Plan Owner", "PLAN_ITEM_ADDED", f"id={p.id} title={p.title}")
        flash("Training plan item added.")
        return redirect(url_for("plan"))
    return render_template("plan.html", items=TrainingPlanItem.query.all(), members=TeamMember.query.all(),
                            skill_list=Skill.query.all(), plan_types=PLAN_TYPES, statuses=PLAN_STATUSES)


@app.route("/plan/<int:item_id>/update", methods=["POST"])
def update_plan(item_id):
    p = TrainingPlanItem.query.get_or_404(item_id)
    old_status = p.status
    p.status = request.form["status"]
    if request.form.get("notes"):
        p.notes = (p.notes + "\n" if p.notes else "") + request.form["notes"]
    db.session.commit()
    log("Training Plan Owner", "PLAN_ITEM_STATUS_CHANGED", f"id={p.id} {old_status} -> {p.status}")
    flash(f"Plan item updated: {old_status} → {p.status}")
    return redirect(url_for("plan"))


@app.route("/audit-log")
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/report")
def report():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    members = TeamMember.query.all()
    all_skills = Skill.query.all()
    assessments = SkillAssessment.query.all()
    certs = Certification.query.all()
    plan_items = TrainingPlanItem.query.all()

    matrix = {}
    for m in members:
        matrix[m.id] = {}
        for s in all_skills:
            a = SkillAssessment.query.filter_by(member_id=m.id, skill_id=s.id).first()
            matrix[m.id][s.id] = a

    gaps = [(a, a.required_level - a.current_level) for a in assessments]
    widest_gaps = sorted(gaps, key=lambda x: x[1], reverse=True)[:5]
    widest_gaps = [g for g in widest_gaps if g[1] > 0]

    total_plan = len(plan_items)
    completed_plan = len([p for p in plan_items if p.status == "Completed"])
    plan_completion_pct = round((completed_plan / total_plan) * 100, 1) if total_plan else 0

    return render_template(
        "report.html", members=members, skill_list=all_skills, matrix=matrix, widest_gaps=widest_gaps,
        certifications=certs, plan_items=plan_items, cert_status=cert_status, today=today,
        plan_completion_pct=plan_completion_pct, levels=LEVELS, generated_at=datetime.utcnow(),
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5012, debug=True)
