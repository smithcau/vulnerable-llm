from db.base import db
import argon2


# Database ORM for Account
class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, name, password, balance=0):
        self.name = name
        self.password = argon2.hash_password(password.encode()).decode("utf-8")

    def login(self, password_guess):
        return argon2.verify_password(self.password.encode(), password_guess.encode())

    def __repr__(self):
        return f"Account name is {self.name} with account number {self.id}"

    @classmethod
    def all_dict(cls):
        return [x.to_json() for x in cls.query.all()]

    def to_json(self):
        return {"name": self.name, "id": self.id}
