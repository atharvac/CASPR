from datetime import datetime

from spar import db, login_manager
from functools import wraps
from flask import redirect, url_for

from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)

class Admin(db.Model, UserMixin):

    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Username: {self.username}"

    @staticmethod
    def check_if_initialized(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            admin_exists = Admin.query.count()
            if not admin_exists:
                return redirect(url_for("main.setup"))
            return func(*args, **kwargs)
        return wrapper