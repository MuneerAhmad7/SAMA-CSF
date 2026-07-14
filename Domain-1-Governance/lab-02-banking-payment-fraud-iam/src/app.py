"""
SecurePay — Lab 02 (Banking Sector)
A payment-system simulator built to reproduce, and then close, the exact
control gaps behind the 2016 Bangladesh Bank / SWIFT heist:
  - Mandatory MFA (TOTP) at login
  - Maker-checker segregation of duties (enforced server-side)
  - Real-time fraud detection rule engine
  - Immutable-style audit log + security dashboard

Run: docker compose up --build   (see ../docker-compose.yml)
Or:  pip install -r requirements.txt && python app.py
"""
import base64
import io
from datetime import datetime

import pyotp
import qrcode
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import fraud_engine

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///securepay.db"
app.config["SECRET_KEY"] = "lab-secret-key-change-me"
db = SQLAlchemy(app)

ISSUER = "SecurePay-Lab02"


# ---------- Models ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Maker / Checker / Admin
    totp_secret = db.Column(db.String(64), nullable=False)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maker_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    beneficiary_name = db.Column(db.String(120))
    beneficiary_account = db.Column(db.String(60))
    beneficiary_country = db.Column(db.String(60))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20), default="Pending")  # Pending/Approved/Rejected
    risk_level = db.Column(db.String(10))
    risk_reasons = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    checker_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    decision_note = db.Column(db.String(300))


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    actor = db.Column(db.String(80))
    action = db.Column(db.String(80))
    details = db.Column(db.String(400))


def log(actor, action, details=""):
    db.session.add(AuditLog(actor=actor, action=action, details=details))
    db.session.commit()


def current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None


def qr_data_uri(secret, username):
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=ISSUER)
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


# ---------- Auth routes ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(username=request.form["username"]).first():
            flash("Username already exists.")
            return redirect(url_for("register"))
        secret = pyotp.random_base32()
        u = User(
            username=request.form["username"],
            password_hash=generate_password_hash(request.form["password"]),
            role=request.form["role"],
            totp_secret=secret,
        )
        db.session.add(u)
        db.session.commit()
        log(u.username, "USER_REGISTERED", f"role={u.role}")
        return render_template("mfa_enroll.html", username=u.username, secret=secret,
                                qr=qr_data_uri(secret, u.username))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = User.query.filter_by(username=request.form["username"]).first()
        if not u or not check_password_hash(u.password_hash, request.form["password"]):
            log(request.form.get("username", "unknown"), "LOGIN_FAILED", "bad username/password")
            flash("Invalid username or password.")
            return redirect(url_for("login"))
        totp = pyotp.TOTP(u.totp_secret)
        if not totp.verify(request.form["totp_code"], valid_window=1):
            log(u.username, "LOGIN_FAILED", "invalid MFA code")
            flash("Invalid MFA code. Login refused — MFA is mandatory.")
            return redirect(url_for("login"))
        session["user_id"] = u.id
        log(u.username, "LOGIN_SUCCESS", f"role={u.role}")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    u = current_user()
    if u:
        log(u.username, "LOGOUT")
    session.clear()
    return redirect(url_for("login"))


# ---------- Payments ----------
@app.route("/payments", methods=["GET", "POST"])
def payments():
    u = current_user()
    if not u:
        return redirect(url_for("login"))

    if request.method == "POST":
        if u.role != "Maker":
            flash("Only Makers can create payments.")
            return redirect(url_for("payments"))

        created_at = datetime.utcnow()
        if request.form.get("simulate_off_hours"):
            created_at = created_at.replace(hour=2, minute=15)

        p = Payment(
            maker_id=u.id,
            beneficiary_name=request.form["beneficiary_name"],
            beneficiary_account=request.form["beneficiary_account"],
            beneficiary_country=request.form["beneficiary_country"],
            amount=float(request.form["amount"]),
            created_at=created_at,
        )
        db.session.add(p)
        db.session.commit()

        all_payments = Payment.query.all()
        risk_level, reasons = fraud_engine.evaluate(p, all_payments)
        p.risk_level = risk_level
        p.risk_reasons = "; ".join(reasons) if reasons else "None"
        db.session.commit()

        log(u.username, "PAYMENT_CREATED",
            f"id={p.id} amount={p.amount} beneficiary={p.beneficiary_name} risk={risk_level}")
        if risk_level in ("HIGH", "MEDIUM"):
            log("FRAUD_ENGINE", f"PAYMENT_FLAGGED_{risk_level}", f"id={p.id} reasons={p.risk_reasons}")
        flash(f"Payment created. Fraud engine risk assessment: {risk_level}.")
        return redirect(url_for("payments"))

    all_payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template("payments.html", payments=all_payments, user=u)


@app.route("/payments/<int:payment_id>/approve", methods=["POST"])
def approve_payment(payment_id):
    u = current_user()
    if not u or u.role != "Checker":
        flash("Only Checkers can approve payments.")
        return redirect(url_for("payments"))

    p = Payment.query.get_or_404(payment_id)

    if p.maker_id == u.id:
        log(u.username, "SOD_VIOLATION_BLOCKED",
            f"Attempted self-approval of payment id={p.id} — blocked by segregation-of-duties control.")
        flash("BLOCKED: You cannot approve your own payment. This attempt has been logged as a "
              "segregation-of-duties violation.")
        return redirect(url_for("payments"))

    p.status = "Approved"
    p.checker_id = u.id
    p.decision_note = request.form.get("note", "")
    db.session.commit()
    log(u.username, "PAYMENT_APPROVED", f"id={p.id} note={p.decision_note}")
    flash(f"Payment {p.id} approved.")
    return redirect(url_for("payments"))


@app.route("/payments/<int:payment_id>/reject", methods=["POST"])
def reject_payment(payment_id):
    u = current_user()
    if not u or u.role != "Checker":
        flash("Only Checkers can reject payments.")
        return redirect(url_for("payments"))

    p = Payment.query.get_or_404(payment_id)
    p.status = "Rejected"
    p.checker_id = u.id
    p.decision_note = request.form.get("note", "")
    db.session.commit()
    log(u.username, "PAYMENT_REJECTED", f"id={p.id} note={p.decision_note}")
    flash(f"Payment {p.id} rejected.")
    return redirect(url_for("payments"))


# ---------- Dashboard & Audit ----------
@app.route("/dashboard")
def dashboard():
    u = current_user()
    if not u:
        return redirect(url_for("login"))

    total = Payment.query.count()
    flagged = Payment.query.filter(Payment.risk_level.in_(["HIGH", "MEDIUM"])).count()
    approved = Payment.query.filter_by(status="Approved").count()
    rejected = Payment.query.filter_by(status="Rejected").count()
    sod_violations = AuditLog.query.filter_by(action="SOD_VIOLATION_BLOCKED").count()
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(25).all()
    high_risk_payments = Payment.query.filter_by(risk_level="HIGH").all()

    return render_template(
        "dashboard.html", user=u, total=total, flagged=flagged, approved=approved,
        rejected=rejected, sod_violations=sod_violations, recent_logs=recent_logs,
        high_risk_payments=high_risk_payments,
    )


@app.route("/audit")
def audit():
    u = current_user()
    if not u:
        return redirect(url_for("login"))
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit.html", logs=logs)


@app.route("/")
def index():
    return redirect(url_for("dashboard")) if current_user() else redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)
