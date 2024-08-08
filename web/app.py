from flask import Flask
from db.base import db
from flask_migrate import Migrate
import uuid
import os
from flask_cors import CORS

# Import views
from views.accounts import app as accounts_view
from views.base import app as base_view
from views.display import app as display_view
from views.chat import app as chat_view

app = Flask(__name__)
app.register_blueprint(accounts_view)
app.register_blueprint(base_view)
app.register_blueprint(display_view)
app.register_blueprint(chat_view)

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_TEST", uuid.uuid4().hex)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["DEBUG"] = True

db.init_app(app)
Migrate(app, db)
cors = CORS(
    app,
    resources={
        r"/api/chat": {
            "origins": [
                "http://127.0.0.1:5000/chat",
                "https://store.cartersmith.com.au/chat",
            ]
        }
    },
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
