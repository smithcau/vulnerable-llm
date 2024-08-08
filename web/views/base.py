from flask import Blueprint, render_template, send_from_directory
import os
from db import Product
from db.base import db

app = Blueprint("base", __name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/seed")
def seed_db():
    for i in [
        ("Apples", 2, "Mmm, yummy apples!"),
        ("Pears", 1, "Home grown pears"),
        ("GPUs", 400, "Artisan GPUs for your LLMs!"),
    ]:
        product = Product(i[0], i[1], i[2])
        db.session.add(product)
        db.session.commit()
    return "ok"


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template("500.html"), 500
