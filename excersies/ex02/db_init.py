# Group work: Nazanin Nakhaie Ahooie, Mehrdad Kaheh, Sepehr Samadi, Danial Khaledi
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("app")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

ctx = app.app_context()
ctx.push()

class StorageItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    location = db.Column(db.String(64), nullable=False)

    product = db.relationship("Product", back_populates="in_storage")
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_storage = db.relationship("StorageItem", back_populates="product")

db.create_all()

p1 = Product(handle="a1", weight=2.5, price=5.3)
p2 = Product(handle="a2", weight=2.7, price=10)
p3 = Product(handle="a3", weight=2.7, price=10)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.commit()

