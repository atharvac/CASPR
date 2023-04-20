from flask import (Blueprint, abort, render_template, request)
from flask_login import login_required
from spar.models.audit_logs import AuditLog

audit_logs = Blueprint(
    "audit_logs",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/audit_logs/static/",
    url_prefix="/logs"
)


@audit_logs.route("/")
@login_required
def index():
    page_number = request.args.get("page", "1")
    if page_number.isnumeric():
        page_number = int(page_number)
    else:
        page_number = 1

    audit_logs = (
        AuditLog.query
        .order_by(AuditLog.created_at.desc())
        .paginate(page=page_number, per_page=10)
    )
    total_count = AuditLog.query.count()

    return render_template(
        "audit_logs/index.html", total_count=total_count, audit_logs=audit_logs
    )



@audit_logs.route("/detail/<audit_log_id>")
@login_required
def detail(audit_log_id):
    log = AuditLog.query.filter_by(
        id=audit_log_id
    ).first()

    if log is None:
        abort(404)


    log_resp = {
        "actor": log.actor,
        "event": log.event,
        "outcome": log.outcome,
        "message": log.message,
        "ip_address": log.ip_address,
        "timestamp": log.created_at,
    }

    return {
        "status": "success",
        "data": log_resp
    }, 200

# add your routes here