import argon2
from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
)
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from logic.forms import CreateForm, LoginForm
from db import Account
from db.base import db

app = Blueprint("accounts", __name__, template_folder="templates")


@app.route("/create", methods=["GET", "POST"])
def create_account():
    form = CreateForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        try:
            new_account = Account(name, password)
            db.session.add(new_account)
            db.session.commit()
        except IntegrityError:
            return render_template(
                "create_account.html", form=form, error="Your username must be unique"
            )
        session["username"] = new_account.name
        return redirect(url_for("display.my_account"))

    return render_template("create_account.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if not (account := Account.query.filter(Account.name == username).first()):
            return render_template(
                "login.html", form=form, error="Invalid username or password"
            )
        try:
            if account.login(password):
                session["username"] = account.name
                return redirect(url_for("display.my_account"))
        except argon2.exceptions.VerifyMismatchError:
            return render_template(
                "login.html", form=form, error="Invalid username or password"
            )
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    session["username"] = None
    return redirect(url_for("base.index"))
