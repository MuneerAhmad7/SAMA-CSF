"""
Seed demo data for the AI Governance & Model Risk Evidence Tracker (Lab 10).
Falak Pay Financial Company (fictional).

Run INSIDE the container:
    docker compose exec ai-governance python seed_demo_data.py

Or locally:
    python seed_demo_data.py

Safe to re-run: skips if data already exists.
"""
import app as a

SYSTEMS = [
    ("Customer Support Chatbot", "Customer Chatbot", "Critical", "Omar Al-Shammari", "gpt-based-v2.3",
     "2026-02-20", "Customer-facing chatbot handling support queries, refund questions, and account "
     "issues. First introduced in Lab 08's project register — this lab picks it up from the AI "
     "governance angle rather than the SDLC angle."),
    ("Fraud Anomaly Detection Model", "Fraud/Anomaly Detection Model", "Critical", "Fatimah Al-Zahrani",
     "fraud-ml-v1.4", "2025-11-01", "ML model flagging anomalous payment patterns to complement the "
     "rule-based fraud engine from Lab 02."),
    ("Credit Scoring Model", "Credit Scoring Model", "High", "Fatimah Al-Zahrani", "credit-model-v3.0",
     "2025-06-15", "Assists loan officers with creditworthiness scoring; final decisions remain human-made."),
    ("Internal Developer Copilot", "Internal Developer Copilot", "Medium", "Layla Al-Ghamdi", "copilot-enterprise",
     "2026-01-10", "Code-completion assistant for the engineering team, internal use only."),
    ("Marketing Content Generator", "Marketing Content Generator", "Low", "Reem Al-Subai'i", "content-gen-v1.1",
     "2025-09-01", "Drafts marketing copy for internal review before publication; no direct customer exposure."),
]

# (system_name, checkpoint_name, trigger, enforced, notes)
CHECKPOINTS = [
    ("Customer Support Chatbot", "Refund / Policy Exception Escalation", "Any refund, compensation, or policy "
     "exception mentioned in the conversation", False,
     "⚠ DOCUMENTED BUT NOT ENFORCED IN PRODUCTION. This is the exact gap behind the Air Canada chatbot ruling — "
     "the checkpoint exists in the design spec but the current chatbot build does not actually force a human "
     "handoff when these topics come up. See the incident below."),
    ("Customer Support Chatbot", "Account Closure / Fraud Report Escalation", "Customer requests account closure "
     "or reports suspected fraud", True, "Enforced — hard-coded handoff to a human agent, verified in Q1 testing."),
    ("Fraud Anomaly Detection Model", "High-Value Transaction Block Escalation", "Model recommends blocking a "
     "transaction over SAR 500,000", True, "Enforced — model output is advisory only above this threshold; "
     "Checker role (see Lab 02) makes the final call."),
    ("Credit Scoring Model", "Automated Decline Escalation", "Model recommends declining a loan application",
     True, "Enforced — all declines require loan officer review before communication to the applicant; no "
     "automated denial is ever sent directly from the model."),
    ("Internal Developer Copilot", "Security-Sensitive Code Suggestion Review", "Suggested code touches "
     "authentication, cryptography, or payment processing logic", False,
     "Not yet enforced — currently relies on standard code review (see Lab 08 Build gate) rather than a "
     "dedicated AI-suggestion flag. Planned for next quarter."),
]

# (system_name, sample_date, sample_size, reviewer, accurate, inaccurate, escalation_needed, notes)
SAMPLES = [
    ("Customer Support Chatbot", "2026-01-15", 50, "Huda Al-Anazi", 46, 4, 2,
     "Routine monthly sample — general support queries, mostly accurate."),
    ("Customer Support Chatbot", "2026-02-15", 50, "Huda Al-Anazi", 38, 12, 9,
     "⚠ Accuracy dropped sharply on policy-sensitive questions (refunds, fee waivers, exceptions) — "
     "9 of 50 sampled conversations should have escalated to a human per the (unenforced) checkpoint above "
     "but did not. This sample batch is what should have triggered the incident below sooner."),
    ("Customer Support Chatbot", "2026-03-15", 50, "Huda Al-Anazi", 41, 9, 3,
     "Improved after the incident response and initial guardrail patch, but still below the 90% target."),
    ("Fraud Anomaly Detection Model", "2026-01-20", 100, "Fatimah Al-Zahrani", 94, 6, 1,
     "Quarterly review against confirmed fraud/legitimate transaction outcomes."),
    ("Fraud Anomaly Detection Model", "2026-03-20", 100, "Fatimah Al-Zahrani", 96, 4, 0,
     "Model retrained on Q1 data, slight accuracy improvement."),
    ("Credit Scoring Model", "2026-02-01", 80, "Noura Al-Qahtani", 74, 6, 0,
     "Reviewed against loan officer override rate — 6 of 80 scores were overridden by human reviewers."),
    ("Internal Developer Copilot", "2026-02-10", 30, "Layla Al-Ghamdi", 27, 3, 3,
     "Manual review of accepted code suggestions; 3 flagged as needing security review before merge."),
]

# (system_name, date, description, severity, root_cause, remediation, status)
INCIDENTS = [
    ("Customer Support Chatbot", "2026-02-18",
     "A customer asked the chatbot about a fee waiver following a family emergency. The chatbot stated the "
     "customer could request the waiver retroactively within 60 days, which does not match Falak Pay's actual "
     "policy requiring the request before the fee is charged. The customer relied on this and later disputed "
     "the charge, citing the chatbot's statement.",
     "High",
     "The Refund / Policy Exception Escalation checkpoint (see Oversight Checkpoints) was documented in the "
     "design specification but never actually enforced in the production chatbot build — a direct replay of "
     "the 2022-2024 Air Canada chatbot case. No sampling review had caught this before the customer complaint; "
     "the February sample batch flagging the drop in accuracy was reviewed but not yet acted on.",
     "1) Fee waived for the affected customer as a goodwill resolution, avoiding an Air Canada-style dispute. "
     "2) Emergency guardrail patch deployed to hard-block any fee/refund/policy-exception language pending full "
     "checkpoint enforcement. 3) Full enforcement of the escalation checkpoint scheduled as the top-priority "
     "model change (see Model Change Log).",
     "Investigating"),
    ("Fraud Anomaly Detection Model", "2026-01-25",
     "Model flagged an unusually high number of legitimate high-volume merchant transactions as anomalous "
     "during a promotional sales event, requiring manual review backlog.",
     "Medium", "Model had not been retrained on seasonal promotional transaction patterns.",
     "Retrained on updated transaction data including promotional period patterns; false-positive rate "
     "improved in the March sample batch.", "Resolved"),
]

# (system_name, date, change_type, description, status, approver)
CHANGES = [
    ("Customer Support Chatbot", "2026-03-01", "Guardrail Update",
     "Enforce the Refund / Policy Exception Escalation checkpoint as a hard technical block, not just a design "
     "intent — directly addressing the incident above.", "Pending", None),
    ("Customer Support Chatbot", "2026-02-19", "Guardrail Update",
     "Emergency patch: block any fee/refund/policy-exception language pending full checkpoint enforcement.",
     "Approved", "Khalid Al-Mutairi"),
    ("Fraud Anomaly Detection Model", "2026-02-01", "Fine-Tuning",
     "Retrain on Q4 2025 promotional-period transaction data to reduce seasonal false positives.",
     "Approved", "Fatimah Al-Zahrani"),
    ("Credit Scoring Model", "2026-01-10", "Model Version Upgrade",
     "Upgrade from credit-model-v2.8 to v3.0, incorporating updated bureau data fields.",
     "Approved", "Khalid Al-Mutairi"),
    ("Internal Developer Copilot", "2026-03-05", "Prompt Change",
     "Add explicit instruction to flag any suggested code touching authentication or payment logic for "
     "mandatory security review.", "Pending", None),
]


def get_or_create_system(name, stype, tier, owner, version, deployed, desc):
    existing = a.AISystem.query.filter_by(name=name).first()
    if existing:
        return existing, False
    s = a.AISystem(name=name, system_type=stype, risk_tier=tier, owner=owner,
                    model_version=version, deployed_date=deployed, description=desc)
    a.db.session.add(s)
    a.db.session.commit()
    return s, True


def main():
    with a.app.app_context():
        a.init_db()

        print("=" * 70)
        print("Seeding AI System Inventory for Falak Pay Financial Company")
        print("=" * 70)
        system_map = {}
        for name, stype, tier, owner, version, deployed, desc in SYSTEMS:
            s, created = get_or_create_system(name, stype, tier, owner, version, deployed, desc)
            system_map[name] = s
            print(f"  [{'CREATED' if created else 'exists'}] {name} ({tier})")

        print()
        print("=" * 70)
        print("Seeding Human Oversight Checkpoints")
        print("=" * 70)
        if a.OversightCheckpoint.query.count() == 0:
            for sys_name, cp_name, trigger, enforced, notes in CHECKPOINTS:
                a.db.session.add(a.OversightCheckpoint(
                    ai_system_id=system_map[sys_name].id, checkpoint_name=cp_name,
                    trigger_condition=trigger, enforced=enforced, notes=notes,
                ))
                flag = " ⚠ NOT ENFORCED (Air Canada pattern)" if not enforced and "Refund" in cp_name else ""
                print(f"  [{'ENFORCED' if enforced else 'NOT ENFORCED':13s}] {sys_name}: {cp_name}{flag}")
            a.db.session.commit()
        else:
            print("  Checkpoints already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Output Sample Review Log")
        print("=" * 70)
        if a.OutputSample.query.count() == 0:
            for sys_name, date, size, reviewer, acc, inacc, esc, notes in SAMPLES:
                a.db.session.add(a.OutputSample(
                    ai_system_id=system_map[sys_name].id, sample_date=date, sample_size=size,
                    reviewer=reviewer, accurate_count=acc, inaccurate_count=inacc,
                    escalation_needed_count=esc, notes=notes,
                ))
                pct = round((acc / size) * 100, 1)
                print(f"  [{pct:5.1f}% accurate] {sys_name} — {date} (n={size})")
            a.db.session.commit()
        else:
            print("  Samples already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding AI Incident Log")
        print("=" * 70)
        if a.Incident.query.count() == 0:
            for sys_name, date, desc, sev, root_cause, remediation, status in INCIDENTS:
                a.db.session.add(a.Incident(
                    ai_system_id=system_map[sys_name].id, incident_date=date, description=desc,
                    severity=sev, root_cause=root_cause, remediation=remediation, status=status,
                ))
                flag = " ⚠ AIR CANADA REPLAY" if "Air Canada" in root_cause else ""
                print(f"  [{sev:8s}] {sys_name} — {date}{flag}")
            a.db.session.commit()
        else:
            print("  Incidents already seeded — skipping.")

        print()
        print("=" * 70)
        print("Seeding Model Change Log")
        print("=" * 70)
        if a.ModelChange.query.count() == 0:
            for sys_name, date, ctype, desc, status, approver in CHANGES:
                a.db.session.add(a.ModelChange(
                    ai_system_id=system_map[sys_name].id, change_date=date, change_type=ctype,
                    description=desc, status=status, approver=approver,
                ))
                print(f"  [{status:10s}] {sys_name} — {ctype}")
            a.db.session.commit()
        else:
            print("  Changes already seeded — skipping.")

        a.log("seed_script", "DEMO_DATA_SEEDED", "Full AI Governance demo dataset loaded")

        all_samples = a.OutputSample.query.all()
        overall = a.sample_accuracy(all_samples)
        print()
        print("=" * 70)
        print(f"Done. {a.AISystem.query.count()} AI systems, {len(all_samples)} sample batches seeded.")
        print(f"Current weighted sample accuracy across all systems: {overall}%")
        print("Visit /dashboard for the overview, or /report for the printable")
        print("board-ready report.")
        print("=" * 70)


if __name__ == "__main__":
    main()
