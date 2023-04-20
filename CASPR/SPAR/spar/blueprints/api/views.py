from flask import Blueprint, render_template, request
from spar.models import AccessTokens
from cerberus import Validator
from .json_request_schema import (
    upload_signing_key_request, remove_signing_key_request, get_signing_key_request,
    ci_cass_status
)
from spar.models.audit_logs import AuditLog
from spar.models import SigningKeys
from spar import db
from hashlib import sha256

api = Blueprint(
    "api",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/api/static/",
    url_prefix="/api"
)


@api.route("/")
def index():
    return render_template("api/index.html", title="Welcome")


@api.route("/signing-key-upload", methods=['POST'])
@AccessTokens.access_token_required
def upload_signing_key():
    request_data = request.get_json()
    v = Validator(upload_signing_key_request)
    if v.validate(request_data):
        pub_key = request_data["public_key"].strip()
        fingerprint = request_data["fingerprint"].strip().lower()
        email = request_data["email"].strip().lower()

        _key = SigningKeys.query.filter_by(fingerprint=fingerprint).first()
        if _key:
            AuditLog.log(
                f"{email}",
                "signing_key.upload",
                "failure",
                f"Signing key upload failed, already exists. fingerprint: {fingerprint}",
                request.access_route
            )
            db.session.commit()
            return (
                {   
                    "status": "failure",
                    "data": {"message": f"{fingerprint} Already Exists"}
                },
                400
            )
        signing_key = SigningKeys(
            fingerprint=fingerprint, public_key=pub_key, email=email
        )

        db.session.add(signing_key)
        AuditLog.log(
            f"{email}",
            "signing_key.upload",
            "success",
            f"Signing key uploaded, fingerprint: {fingerprint}",
            request.access_route
        )
        db.session.commit()
        return (
            {
                "status": "success",
                "data":{"messsage": "Signing key uploaded successfully"}
            },
            200
        )

    AuditLog.log(
        f"{email}",
        "signing_key.upload",
        "failure",
        f"Signing key upload failed, invalid request. fingerprint: {fingerprint}",
        request.access_route
    )
    db.session.commit()
    return (
        {
            "status": "failure",
            "data": {"message": "Schema validation error"}
        },
        400
    )

@api.route("/signing-key-remove", methods=['POST'])
@AccessTokens.access_token_required_return
def remove_signing_key(access_token):
    request_data = request.get_json()
    v = Validator(remove_signing_key_request)
    if v.validate(request_data):
        fingerprint = request_data["fingerprint"].strip().lower()

        _key = SigningKeys.query.filter_by(fingerprint=fingerprint).first()
        if not _key:
            AuditLog.log(
                f"{access_token.name}",
                "signing_key.remove",
                "failure",
                f"Signing key not found. fingerprint: {fingerprint}",
                request.access_route
            )
            db.session.commit()
            return (
                {   
                    "status": "failure",
                    "data": {"message": f"Key {fingerprint} Doesn't Exist"}
                },
                400
            )
        AuditLog.log(
            f"{access_token.name}",
            "signing_key.remove",
            "success",
            f"Signing key removed. fingerprint: {fingerprint}",
            request.access_route
        )
        db.session.delete(_key)
        db.session.commit()

        return (
            {
                "status": "success",
                "data":{"messsage": "Signing key removed successfully"}
            },
            200
        )

    return (
        {
            "status": "failure",
            "data": {"message": "Schema validation error"}
        },
        400
    )

@api.route("/get-signing-key", methods=['POST'])
@AccessTokens.access_token_required_return
def get_signing_key(access_token):
    request_data = request.get_json()
    v = Validator(get_signing_key_request)
    if v.validate(request_data):
        keyid = request_data["keyid"].strip().lower()
        if len(keyid) < 16:
            AuditLog.log(
                f"{access_token.name}",
                "signing_key.request",
                "failure",
                f"Signing key not found. key ID: {keyid}",
                request.access_route
            )
            db.session.commit()
            return (
                {   
                    "status": "failure",
                    "data": {"message": f"KeyID {keyid} is invalid"}
                },
                400
            ) 
        _key = SigningKeys.query.filter(
            SigningKeys.fingerprint.like(f"%{keyid}")
        ).first()

        if _key:
            AuditLog.log(
                f"{access_token.name}",
                "signing_key.request",
                "success",
                f"Public key sent successfully. key ID: {keyid}",
                request.access_route
            )
            db.session.commit()
            return (
                {
                    "status": "success",
                    "data":{"publickey": _key.public_key}
                },
                200
            )
        else:
            AuditLog.log(
                f"{access_token.name}",
                "signing_key.request",
                "failure",
                f"Signing key not found. key ID: {keyid}",
                request.access_route
            )
            db.session.commit()
            return (
                {   
                    "status": "failure",
                    "data": {"message": f"Key {keyid} Doesn't Exist"}
                },
                400
            )
    return (
        {
            "status": "failure",
            "data": {"message": "Schema validation error"}
        },
        400
    )



@api.route("/ci-status", methods=['POST'])
@AccessTokens.access_token_required
def ci_status():
    request_data = request.get_json()
    v = Validator(ci_cass_status)
    if v.validate(request_data):
        status = request_data.get("status")
        keyid = request_data.get("keyid")
        email = request_data.get("email")

        if status == "success":
            AuditLog.log(
                email,
                "ci.result",
                status,
                f"CI pipeline passed. Key ID: {keyid}",
                request.access_route
            )
        else:
            AuditLog.log(
                email,
                "ci.result",
                status,
                f"CI pipeline failed. Key ID: {keyid}",
                request.access_route
            )
        db.session.commit()
        return ({"status": "success"}, 200)       
    
    return (
        {
            "status": "failure",
            "data": {"message": "Schema validation error"}
        },
        400 
    )

# add your routes here