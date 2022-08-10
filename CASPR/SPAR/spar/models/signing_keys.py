from datetime import datetime

from spar import db


class SigningKeys(db.Model):

    __tablename__ = "signing_keys"

    fingerprint = db.Column(db.String(255), nullable=False, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    public_key = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Signing Key: {self.fingerprint}"

    @property
    def keyid(self):
        if not self.fingerprint:
            return None
        return self.fingerprint[-16:]