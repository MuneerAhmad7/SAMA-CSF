"""
Remediation SLA logic for audit findings — distinct from Lab 03's patch SLAs,
since audit findings often involve broader remediation work (process changes,
infrastructure hardening) rather than a single patch deployment.

Typical audit remediation SLA convention used here:
Critical: 30 days | High: 60 days | Medium: 90 days | Low: 180 days
"""
from datetime import timedelta

SLA_DAYS = {
    "Critical": 30,
    "High": 60,
    "Medium": 90,
    "Low": 180,
}

CLOSED_STATUSES = {"Remediated", "Verified Closed"}


def due_date(identified_at, severity):
    days = SLA_DAYS.get(severity, 90)
    return identified_at + timedelta(days=days)


def is_overdue(finding, now):
    if finding.status in CLOSED_STATUSES:
        return False
    return now > due_date(finding.identified_at, finding.severity)


def days_overdue(finding, now):
    if not is_overdue(finding, now):
        return 0
    return (now - due_date(finding.identified_at, finding.severity)).days
