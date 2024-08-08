from flask import Blueprint, render_template, session, redirect, url_for, request
from db import Transaction, Account, Product
from db.base import db
from logic.forms import BuyForm

app = Blueprint("display", __name__, template_folder="templates")


@app.route("/account", methods=["GET", "POST"])
def my_account():
    if account := Account.query.filter_by(name=session.get("username")).first():
        products = Product.query.all()
        return render_template("my_account.html", products=products, account=account)
    return redirect(url_for("accounts.login"))


@app.route("/transactions", methods=["GET", "POST"])
def get_transactions():
    if account := Account.query.filter_by(name=session.get("username")).first():
        transactions = Transaction.query.filter(
            Transaction.account_id == account.id
        ).all()
        return render_template(
            "transactions.html", transactions=transactions, account=account
        )
    return redirect(url_for("accounts.login"))


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if account := Account.query.filter_by(name=session.get("username")).first():
        return render_template("chat.html", account=account)
    return redirect(url_for("accounts.login"))


@app.route("/buy/<item_id>", methods=["GET", "POST"])
def buy(item_id):
    if product := Product.query.get(item_id):
        if account := Account.query.filter_by(name=session.get("username")).first():
            form = BuyForm()
            if form.validate_on_submit():
                transaction = Transaction(product.name, form.qty.data, account.id)
                db.session.add(transaction)
                db.session.commit()
                return redirect(url_for("display.get_transactions"))
            return render_template(
                "buy.html", form=form, account=account, product=product
            )
    return redirect(url_for("display.my_account"))
