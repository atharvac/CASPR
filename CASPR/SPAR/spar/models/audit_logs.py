from datetime import datetime

from spar import db
from uuid import uuid4


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(), unique=True, nullable=False)
    actor = db.Column(db.String(255), nullable=False)
    event = db.Column(db.String(255), nullable=False)
    outcome = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    ip_address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return "Audit Log: {}".format(self.message)
    
    @staticmethod
    def log(actor, event, outcome, message, ip):
        audit_log = AuditLog(
            public_id=uuid4(),
            actor=actor,
            event=event,
            outcome=outcome,
            message=message,
            ip_address=ip,
        )
        db.session.add(audit_log)
        # db.session.commit()