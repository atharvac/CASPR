from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class AdminRegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your Username"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter Password"}
    )
    submit = SubmitField("Next")


class AdminLoginForm(AdminRegisterForm):
    pass


class AccessTokenForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter Name"},
    )
    submit = SubmitField("Create") 