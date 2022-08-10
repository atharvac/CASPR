from os import access
from flask import Blueprint, redirect, render_template, url_for, flash
from .forms import AdminRegisterForm, AdminLoginForm, AccessTokenForm
from spar.models.admin import Admin
from spar.models.access_tokens import AccessTokens
import bcrypt
from spar import db
from flask_login import login_user, login_required, logout_user
from secrets import token_urlsafe
from hashlib import sha256


main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/main/static/",
    url_prefix="/"
)


@main.route("/")
@login_required
def index():
    tokens = AccessTokens.query.all()
    return render_template("main/index.html", title="Tokens", tokens=tokens)


@main.route("/access-token-create", methods=['GET', 'POST'])
@login_required
def create_access_token():
    form = AccessTokenForm()
    if form.validate_on_submit():
        generated_token = token_urlsafe(32)
        access_token = AccessTokens(
            name=form.name.data,
            access_token=sha256(generated_token.encode()).hexdigest()
        )
        db.session.add(access_token)
        db.session.commit()
        flash(f"Access Token:{generated_token}", "success")
        return redirect(url_for("main.index"))
    return render_template("main/access_token_create.html", form=form, title="Login") 



@main.route("/remove-access-token/<token_hash>", methods=['GET'])
@login_required
def remove_access_token(token_hash):
    access_token = AccessTokens.query.filter_by(access_token=token_hash).first()
    db.session.delete(access_token)
    db.session.commit()
    flash("Removed access token!", "success")
    return redirect(url_for("main.index"))


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully!", "success")
    return redirect(url_for("main.login"))


@main.route("/login", methods=['GET', 'POST'])
@Admin.check_if_initialized
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        pwd_bytes = form.password.data.encode('utf-8')
        admin = Admin.query.filter_by(username=form.username.data).first()
        if not admin:
            flash("User not found!")
            return redirect(url_for("main.login"))
        pwd_hash = admin.password.encode()
        result = bcrypt.checkpw(pwd_bytes, pwd_hash)
        if not result:
            flash("Incorrect Password!")
            return redirect(url_for("main.login"))
        login_user(admin)
        return redirect(url_for("main.index"))
    return render_template("main/login.html", form=form, title="Login")


@main.route("/setup", methods=['GET', 'POST'])
def setup():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        pwd_bytes = form.password.data.encode('utf-8')
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        pwd_hash = bcrypt.hashpw(pwd_bytes, salt).decode()
        admin = Admin(
            username=form.username.data,
            password=pwd_hash
        )
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for("main.login"))
    return render_template("main/create_admin.html", form=form, title="Setup")


# add your routes here