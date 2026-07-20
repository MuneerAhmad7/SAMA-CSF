from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class GRCItem(db.Model):
    """A single Governance, Risk, or Compliance register item."""
    __tablename__ = "grc_items"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)          # Governance / Risk Management / Compliance
    subcategory = db.Column(db.String(100), nullable=False)
    grc_item = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    objective = db.Column(db.Text)
    owner = db.Column(db.String(120))
    status = db.Column(db.String(30), default="Not Started")     # Not Started/In Progress/Implemented/Reviewed/Approved
    due_date = db.Column(db.String(20))
    implementation_steps = db.Column(db.Text)
    testing_method = db.Column(db.Text)
    risk_level = db.Column(db.String(20))                        # Low/Medium/High/Critical
    mitigation_strategy = db.Column(db.Text)
    compliance_standard = db.Column(db.String(150))
    mock_data_example = db.Column(db.Text)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Policy(db.Model):
    """A governance policy that employees must read and acknowledge."""
    __tablename__ = "policies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80))
    description = db.Column(db.Text)
    version = db.Column(db.String(20), default="1.0")
    effective_date = db.Column(db.String(20))

    acknowledgments = db.relationship(
        "Acknowledgment", backref="policy", cascade="all, delete-orphan"
    )

    def ack_count(self):
        return len(self.acknowledgments)


class Acknowledgment(db.Model):
    """Simulates an employee acknowledging a policy (Policy Management control)."""
    __tablename__ = "acknowledgments"

    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), nullable=False)
    employee_name = db.Column(db.String(120), nullable=False)
    acknowledged_at = db.Column(db.DateTime, default=datetime.utcnow)


class Incident(db.Model):
    """Simulates the Security Incident Response Plan / Incident Response control."""
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20), default="Medium")        # Low/Medium/High/Critical
    status = db.Column(db.String(30), default="Open")            # Open/Investigating/Contained/Resolved
    reported_by = db.Column(db.String(120))
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
