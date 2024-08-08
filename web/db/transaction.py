from db.base import db
from datetime import datetime, timezone


# Database ORM for Transactions
class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    account = db.relationship("Account", backref=db.backref("transactions", lazy=True))

    def __init__(self, item, quantity, account_id):
        self.item = item
        self.quantity = quantity
        self.account_id = account_id

    def __repr__(self):
        return f"Transaction {self.id}: {self.item} x {self.quantity}"

    @classmethod
    def all_dict(cls):
        return [x.to_json() for x in cls.query.all()]

    def to_json(self):
        return {
            "item": self.item,
            "qty": self.quantity,
            "user_id": self.account.id,
            "date": self.date,
        }
