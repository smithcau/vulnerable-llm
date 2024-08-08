from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    IntegerField,
)
from wtforms.validators import InputRequired, EqualTo


class CreateForm(FlaskForm):
    name = StringField("Name of Account: ", [InputRequired()])
    password = PasswordField(
        "Account password",
        [InputRequired(), EqualTo("pwd_confirm", message="Passwords must match")],
    )
    pwd_confirm = PasswordField("Confirm account password")
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    username = StringField("Username: ", [InputRequired()])
    password = PasswordField("Password: ", [InputRequired()])
    submit = SubmitField("Login")


class BuyForm(FlaskForm):
    qty = IntegerField("Quantity: ", [InputRequired()])
    submit = SubmitField("Buy")
