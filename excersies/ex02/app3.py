from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

class ProductConverter(BaseConverter):
    def to_python(self, handle):
        db_product = Product.query.filter_by(handle=handle).first()
        if db_product is None:
            raise NotFound
        return db_product
        
    def to_url(self, db_product):
        return db_product.handle

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
        products = Product.query.all()
        res = []
        for product in products:
            res.append({"handle": product.handle,
                         "weight": f"{product.weight} kg", 
                         "price": product.price})
        return res, 200
    
    def post(self):
        response = Response()
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
        
        response.status = 201
        response.headers['Location'] = f'/api/products/{handle}/'
        return response

class ProductItem(Resource):
    def get(self, handle):
        return Response(status=501)

app.url_map.converters["product"] = ProductConverter
api.add_resource(ProductCollection, "/api/products/")
api.add_resource(ProductItem, "/api/products/<product:product>/")
