from datetime import datetime

from spar import db
from functools import wraps
from flask import request
from hashlib import sha256

class AccessTokens(db.Model):

    __tablename__ = "access_tokens"
    name = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Access-Token-hash: {self.access_token}"


    @staticmethod
    def access_token_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            access_token_req = request.headers.get("Access-Token")
            access_token_hash = sha256(access_token_req.encode()).hexdigest()
            access_token = AccessTokens.query.filter_by(access_token=access_token_hash).first()
            if not access_token:
                return {"Error": "Access Token is invalid"}, 401
            return func(*args, **kwargs)
        return wrapper
    

    @staticmethod
    def access_token_required_return(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            access_token_req = request.headers.get("Access-Token")
            access_token_hash = sha256(access_token_req.encode()).hexdigest()
            access_token = AccessTokens.query.filter_by(access_token=access_token_hash).first()
            if not access_token:
                return {"Error": "Access Token is invalid"}, 401
            return func(access_token, *args, **kwargs)
        return wrapper