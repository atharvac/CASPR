from flask import Blueprint, render_template, request, redirect, flash, url_for
from spar import db
from spar.models.signing_keys import SigningKeys
from spar.models.audit_logs import AuditLog
from flask_login import login_required


signing_keys = Blueprint(
    "signing_keys",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/audit_logs/static/",
    url_prefix="/keys"
)


@signing_keys.route("/")
@login_required
def index():
    page_number = request.args.get("page", "1")
    if page_number.isnumeric():
        page_number = int(page_number)
    else:
        page_number = 1

    signing_keys = (
        SigningKeys.query
        .order_by(SigningKeys.created_at.desc())
        .paginate(page=page_number, per_page=10)
    )
    total_count = SigningKeys.query.count()

    return render_template(
        "signing_keys/index.html", total_count=total_count, signing_keys=signing_keys
    )

@signing_keys.route("/remove/<fingerprint>")
@login_required
def remove_signing_key(fingerprint):
    key = SigningKeys.query.filter_by(fingerprint=fingerprint).first()
    if key:
        db.session.delete(key)
        AuditLog.log(
            "Admin",
            "signing_key.remove",
            "success",
            f"Removed signing key: {fingerprint}",
            request.access_route
        )
        db.session.commit()
        flash("Removed signing key successfully!", "success")
    return redirect(url_for("signing_keys.index"))

# add your routes here