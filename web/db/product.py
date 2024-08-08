from db.base import db
from datetime import datetime


# Database ORM for Products
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

    def __init__(self, item, price, description):
        self.name = item
        self.price = price
        self.description = description

    def __repr__(self):
        return f"Product {self.id}: {self.name} - ${self.price}"

    @classmethod
    def all_dict(cls):
        return [x.to_json() for x in cls.query.all()]

    def to_json(self):
        return {"name": self.name, "price": self.price, "description": self.description}
