"""
Seed demo data for SecurePay (Lab 02) — Falak Pay Financial Company (fictional).

Creates realistic test users and a set of transactions that exercise every
fraud rule in fraud_engine.py, so you can demo the lab immediately without
manually clicking through registration for each scenario.

Run INSIDE the container (recommended, so it uses the same DB the app uses):
    docker compose exec securepay python seed_demo_data.py

Or locally (matches app.py's sqlite:///securepay.db in the same folder):
    python seed_demo_data.py

Safe to re-run: it skips users/payments that already exist.
"""
from datetime import datetime, timedelta

import pyotp

import app
import fraud_engine
from werkzeug.security import generate_password_hash

DEMO_PASSWORD = "FalakPay@2026"

USERS = [
    # username           role
    ("Yousef.AlHarbi",   "Maker"),
    ("Fahad.AlOtaibi",   "Maker"),
    ("Noura.AlQahtani",  "Checker"),
    ("Sara.AlDosari",    "Checker"),
    ("Khalid.AlMutairi", "Admin"),
]


def get_or_create_user(username, role):
    u = app.User.query.filter_by(username=username).first()
    if u:
        return u, False
    secret = pyotp.random_base32()
    u = app.User(
        username=username,
        password_hash=generate_password_hash(DEMO_PASSWORD),
        role=role,
        totp_secret=secret,
    )
    app.db.session.add(u)
    app.db.session.commit()
    return u, True


def create_payment(maker, beneficiary_name, beneficiary_account, beneficiary_country,
                    amount, created_at, all_payments_cache):
    p = app.Payment(
        maker_id=maker.id,
        beneficiary_name=beneficiary_name,
        beneficiary_account=beneficiary_account,
        beneficiary_country=beneficiary_country,
        amount=amount,
        created_at=created_at,
    )
    app.db.session.add(p)
    app.db.session.commit()

    risk_level, reasons = fraud_engine.evaluate(p, all_payments_cache)
    p.risk_level = risk_level
    p.risk_reasons = "; ".join(reasons) if reasons else "None"
    app.db.session.commit()

    app.log(maker.username, "PAYMENT_CREATED",
            f"id={p.id} amount={p.amount} beneficiary={p.beneficiary_name} risk={risk_level}")
    if risk_level in ("HIGH", "MEDIUM"):
        app.log("FRAUD_ENGINE", f"PAYMENT_FLAGGED_{risk_level}", f"id={p.id} reasons={p.risk_reasons}")

    all_payments_cache.append(p)
    return p


def main():
    with app.app.app_context():
        app.db.create_all()

        print("=" * 70)
        print("Seeding demo users for Falak Pay Financial Company (fictional)")
        print("=" * 70)

        created_users = {}
        for username, role in USERS:
            u, was_created = get_or_create_user(username, role)
            created_users[username] = u
            status = "CREATED" if was_created else "already exists"
            print(f"  [{status}] {username:20s} role={role}")

        print()
        print("Login credentials (all demo users share the same password):")
        print(f"  Password: {DEMO_PASSWORD}")
        print()
        print(f"{'Username':20s} {'Role':10s} {'TOTP Secret (add to authenticator app)'}")
        print("-" * 70)
        for username, u in created_users.items():
            print(f"{username:20s} {u.role:10s} {u.totp_secret}")

        # Save credentials to a file too
        with open("DEMO_CREDENTIALS.md", "w") as f:
            f.write("# Demo Credentials — Falak Pay / SecurePay Lab 02\n\n")
            f.write(f"All demo users share the password: `{DEMO_PASSWORD}`\n\n")
            f.write("| Username | Role | TOTP Secret |\n|---|---|---|\n")
            for username, u in created_users.items():
                f.write(f"| {username} | {u.role} | `{u.totp_secret}` |\n")
            f.write("\nAdd each TOTP secret to Google Authenticator / Authy manually "
                     "(\"enter a setup key\"), issuer name can be anything, "
                     "account name = the username above.\n")
        print("\nSaved credentials to DEMO_CREDENTIALS.md")

        # ---- Seed realistic transactions ----
        print()
        print("=" * 70)
        print("Seeding demo transactions (covering every fraud rule)")
        print("=" * 70)

        maker1 = created_users["Yousef.AlHarbi"]
        maker2 = created_users["Fahad.AlOtaibi"]

        existing_payments = app.Payment.query.all()

        if app.Payment.query.count() == 0:
            business_hours_time = datetime.utcnow().replace(hour=11, minute=0, second=0, microsecond=0)
            off_hours_time = datetime.utcnow().replace(hour=2, minute=15, second=0, microsecond=0)

            # 1. Clean, legitimate payment - repeat beneficiary, business hours, low value
            p1 = create_payment(
                maker1, "Al Bilad Trading Est.", "SA-1122334455", "Saudi Arabia",
                45000, business_hours_time, existing_payments,
            )
            print(f"  Payment {p1.id}: LOW risk (legit domestic, repeat beneficiary) -> {p1.risk_level}")

            # 2. Same beneficiary again -> now becomes "repeat", still clean, business hours
            p2 = create_payment(
                maker1, "Al Bilad Trading Est.", "SA-1122334455", "Saudi Arabia",
                60000, business_hours_time + timedelta(days=1), existing_payments,
            )
            print(f"  Payment {p2.id}: repeat beneficiary, still low value -> {p2.risk_level}")

            # 3. THE HEIST REPLAY: high value + new beneficiary + off-hours + high-risk country
            p3 = create_payment(
                maker2, "Rizal Trading Ltd", "PH-9988776655", "Philippines",
                18_500_000, off_hours_time, existing_payments,
            )
            print(f"  Payment {p3.id}: HIGH-VALUE + NEW BENEFICIARY + OFF-HOURS (heist replay) -> {p3.risk_level}")
            print(f"    Reasons: {p3.risk_reasons}")

            # 4. High-risk country flag (using the placeholder watchlist entry)
            p4 = create_payment(
                maker2, "Global Import Co", "TH-4455667788", "Test-HighRisk-Country",
                200_000, business_hours_time, existing_payments,
            )
            print(f"  Payment {p4.id}: HIGH-RISK COUNTRY -> {p4.risk_level}")
            print(f"    Reasons: {p4.risk_reasons}")

            # 5-7. Velocity check: 3 rapid transfers to the same new beneficiary within 30 min
            base_time = business_hours_time.replace(hour=14, minute=0)
            v_account = "AE-5566778899"
            for i in range(3):
                pv = create_payment(
                    maker1, "Sunrise Holdings FZE", v_account, "United Arab Emirates",
                    250_000, base_time + timedelta(minutes=i * 10), existing_payments,
                )
                print(f"  Payment {pv.id}: velocity test transfer #{i+1} -> {pv.risk_level}"
                      f"{' -- ' + pv.risk_reasons if pv.risk_level != 'LOW' else ''}")

            app.db.session.commit()
        else:
            print("  Payments already seeded — skipping (delete securepay.db to reset).")

        print()
        print("=" * 70)
        print("Done. Start the app and log in with any username above + "
              "DEMO_CREDENTIALS.md password + a live TOTP code from your authenticator app.")
        print("=" * 70)


if __name__ == "__main__":
    main()
