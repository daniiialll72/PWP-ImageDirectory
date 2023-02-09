from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/products/add/", methods=["POST"])
def add_product():
    if request.content_type != "application/json":
        return "Request content type must be JSON", 415
    if request.method != "POST":
        return "POST method required", 405
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
    product = Product(
            handle=handle,
            weight=weight,
            price=price
        )
    db.session.add(product)
    db.session.commit()
    return "", 201

@app.route("/storage/<product>/add/", methods=["POST"])
def add_to_storage(product):
    if request.content_type != "application/json":
        return "Request content must be JSON", 415
    if request.method != "POST":
        return "POST method required", 405
    try:
        location = request.json["location"]
        qty = request.json["qty"]
    except:
        return "Incomplete request - missing fields", 400
    try:
        qty = int(qty)
    except:
        return "Qty must be an integer", 400
    try:
        p = Product.query.filter_by(handle=product).first()
        if p:
            item = StorageItem(
                location=location,
                qty=qty,
                product=p)
            db.session.add(item)
            db.session.commit()
            return "", 201
        else:
            return "Product not found", 404
    except:
        return "Product not found", 404

@app.route("/storage/", methods=["POST", "GET"])
def get_inventory():
    if request.content_type == "POST":
        return "GET method required", 405
    products = Product.query.all()
    res = []
    for p in products:
        inventory = StorageItem.query.filter_by(product_id=p.id).all()
        inv = []
        for i in inventory:
            temp = []
            temp.append(i.location)
            temp.append(i.qty)
            inv.append(temp)
        dict = {"handle": p.handle, "weight": p.weight, "price": p.price, "inventory": inv}
        res.append(dict)			
    return jsonify(res), 200		

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