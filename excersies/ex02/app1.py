from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

class StorageItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    location = db.Column(db.String(64), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product", back_populates="in_storage")
	
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)	
    in_storage = db.relationship("StorageItem", back_populates="product")

class ProductCollection(Resource):
    def get(self):
        products = Product.query.order_by(Product.handle).all()
        res = []
        for product in products:
            res.append({"handle": product.handle, 
                        "weight": product.weight, 
                        "price": product.price})
        return res, 200
    
    def post(self):
        if not request.json:
            return 415
        if request.json["weight"] is None or request.json["price"] is None:
            return "Incomplete request - missing fields", 400
        try:
            handle = request.json["handle"]
        except:
            return "Incomplete request - missing fields", 400
        try:
            weight = float(request.json["weight"])
            price = float(request.json["price"])
        except:    
            return "Weight and price must be numbers", 400
        if Product.query.filter_by(handle=handle).all() != []:
            return "Handle already exists", 409	
        try:
            product = Product(
                handle=handle,
                weight=weight,
                price=price
            )
            db.session.add(product)
            db.session.commit()
        except KeyError:
            return 400
        
        return "", 201

api.add_resource(ProductCollection, "/api/products/")
