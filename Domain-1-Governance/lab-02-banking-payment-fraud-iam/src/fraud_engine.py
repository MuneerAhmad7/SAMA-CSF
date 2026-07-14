"""
Fraud detection rule engine — modeled directly on the Bangladesh Bank / SWIFT
heist pattern (2016): high-value transfers to first-time beneficiaries,
submitted outside business hours, in rapid succession, to high-risk
destinations.

Each rule returns (triggered: bool, reason: str | None).
"""
from datetime import datetime, timedelta

HIGH_VALUE_THRESHOLD = 1_000_000  # SAR
VELOCITY_WINDOW_MINUTES = 30
VELOCITY_MAX_COUNT = 2
BUSINESS_HOURS_START = 8
BUSINESS_HOURS_END = 18

HIGH_RISK_COUNTRIES = {"North Korea", "Iran", "Syria", "Test-HighRisk-Country"}


def rule_new_beneficiary_high_value(payment, prior_payments_to_beneficiary):
    if payment.amount >= HIGH_VALUE_THRESHOLD and len(prior_payments_to_beneficiary) == 0:
        return True, f"High-value transfer (SAR {payment.amount:,.0f}) to a first-time beneficiary."
    return False, None


def rule_off_hours(payment):
    hour = payment.created_at.hour
    if hour < BUSINESS_HOURS_START or hour >= BUSINESS_HOURS_END:
        return True, f"Submitted outside business hours ({payment.created_at.strftime('%H:%M')})."
    return False, None


def rule_velocity(payment, recent_payments_to_beneficiary):
    window_start = payment.created_at - timedelta(minutes=VELOCITY_WINDOW_MINUTES)
    count = sum(1 for p in recent_payments_to_beneficiary if p.created_at >= window_start)
    if count >= VELOCITY_MAX_COUNT:
        return True, f"{count} transfers to the same beneficiary within {VELOCITY_WINDOW_MINUTES} minutes."
    return False, None


def rule_high_risk_country(payment):
    if payment.beneficiary_country in HIGH_RISK_COUNTRIES:
        return True, f"Beneficiary country '{payment.beneficiary_country}' is on the high-risk watchlist."
    return False, None


def evaluate(payment, all_payments):
    """
    payment: the Payment being evaluated
    all_payments: list of all prior Payment records (for beneficiary history / velocity)
    Returns: (risk_level: str, reasons: list[str])
    """
    reasons = []

    same_beneficiary = [
        p for p in all_payments
        if p.beneficiary_account == payment.beneficiary_account and p.id != payment.id
    ]

    for triggered, reason in [
        rule_new_beneficiary_high_value(payment, same_beneficiary),
        rule_off_hours(payment),
        rule_velocity(payment, same_beneficiary),
        rule_high_risk_country(payment),
    ]:
        if triggered:
            reasons.append(reason)

    if len(reasons) >= 2:
        risk_level = "HIGH"
    elif len(reasons) == 1:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return risk_level, reasons
