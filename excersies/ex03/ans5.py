import json
#from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event
from werkzeug.routing import BaseConverter

from flask_restful import Resource, Api
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
#from hub.utils import InventoryBuilder, create_error_response

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

MASON = "application/vnd.mason+json"

PRODUCT_PROFILE = "/profiles/product/"
LINK_RELATIONS_URL = "/musicmeta/link-relations/"
ERROR_PROFILE = "/profiles/error-profile/"

@app.route("/api/")
def entry_point():
    products = Product.query.all()

    data = InventoryBuilder()
    data.add_namespace("storage", LINK_RELATIONS_URL)
    data.add_control("profile", href=PRODUCT_PROFILE)
    data.add_control_all_products()
    data.add_control_add_product()
    data["items"] = []

    for prod in products:
        item = MasonBuilder(prod.serialize(short_form=True))
        item.add_control("self", api.url_for(ProductItem, product=prod))
        data["items"].append(item)

    return Response(json.dumps(data), 200, mimetype=MASON)

def create_error_response(status_code, title, message=None):
    resource_url = request.path
    data = MasonBuilder(resource_url=resource_url)
    data.add_error(title, message)
    data.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(data), status_code, mimetype=MASON)


class StorageItem(db.Model):
    location = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product", back_populates="storageItems")
    # sensor = db.relationship("Sensor", back_populates="measurements")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), nullable=False, unique=True)
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    storageItems = db.relationship("StorageItem", back_populates="product")
    # measurements = db.relationship("Measurement", back_populates="sensor")

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["handle", "weight", "price"]
        }
        props = schema["properties"] = {}
        props["handle"] = {
            "description": "Product's unique name",
            "type": "string"
        }
        props["weight"] = {
            "description": "Product's unique name",
            "type": "number"
        }
        props["price"] = {
            "description": "Name of the Product's model",
            "type": "number"
        }
        return schema

    def serialize(self, short_form=False):
        data = InventoryBuilder(
            handle=self.handle,
            weight=self.weight,
            price=self.price
        )

        return data

    def deserialize(self, doc):
        self.name = doc["handle"]
        self.model = doc["weight"]
        self.price = doc["price"]


class ProductConverter(BaseConverter):

    def to_python(self, handle):
        
        db_prod = Product.query.filter_by(handle=handle).first()

        if db_prod is None:
            raise NotFound

        return db_prod

    def to_url(self, db_prod):
      
        return db_prod.handle

class ProductItem(Resource):
    def get(self, product):
        prod = Product.query.filter_by(handle=product.handle).first()
        if not prod:
            return create_error_response(404, "handle not found")

        data = product.serialize()
        data.add_namespace("storage", LINK_RELATIONS_URL)
        data.add_control("self", api.url_for(ProductItem, product=product))

        data.add_control("profile", href=PRODUCT_PROFILE)
        data.add_control("collection", href=url_for("productcollection"))
        data.add_control_edit_product(product=product,handle=product.handle)
        data.add_control_delete_product(product=product,handle=product.handle)
        return Response(json.dumps(data), 200, mimetype=MASON)

    def delete(self, product):
        prod = Product.query.filter_by(handle=product.handle).first()
        if not prod:
            return create_error_response(404, "Product not found")
        try:
            db.session.delete(prod)
            db.session.commit()
        except:
            return create_error_response(500, "Database error")

        return Response(status= 204, mimetype=MASON)

    def put(self, product):
        prod = Product.query.filter_by(handle=product.handle).first()
        if not prod:
            return create_error_response(404, "Product not found")

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Use JSON")

        try:
            validate(
                request.json,
                prod.json_schema()
            )

        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        
        prod.handle = request.json["handle"]
        prod.weight = request.json["weight"]
        prod.price = request.json["price"]

        try:
            db.session.add(prod)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409, "Position reserved",
                "Product already exist"
        )
        except:
            return create_error_response(500, "Database error")

        return Response(status= 204, mimetype=MASON)

class ProductCollection(Resource):

    def get(self):
        products = Product.query.all()

        data = InventoryBuilder()
        data.add_namespace("storage", LINK_RELATIONS_URL)
        data.add_control("profile", href=PRODUCT_PROFILE)
        data.add_control_all_products()
        data.add_control_add_product()
        data["items"] = []

        for prod in products:
            item = MasonBuilder(prod.serialize(short_form=True))
            item.add_control("self", api.url_for(ProductItem, product=prod))
            data["items"].append(item)

        
        return Response(json.dumps(data), 200, mimetype=MASON)


    

    def post(self):

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Use JSON")

        try:
            validate(
                request.json,
                Product.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        prod = Product(
            handle=request.json['handle'],
            weight=request.json["weight"],
            price=request.json["price"],
        )

        try:
            db.session.add(prod)
            db.session.commit()
        except:
            return create_error_response(409, "Database error")

        return Response(
            status=201,
            headers={"Location": url_for("productitem", product=prod)}
        )
class MasonBuilder(dict):
    

    DELETE_RELATION = ""

    def add_error(self, title, details):
        

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

    def add_control_post(self, ctrl_name, title, href, schema):
        

        self.add_control(
            ctrl_name,
            href,
            method="POST",
            encoding="json",
            title=title,
            schema=schema
        )

    def add_control_put(self, title, href, schema):
        
        self.add_control(
            "edit",
            href,
            method="PUT",
            encoding="json",
            title=title,
            schema=schema
        )

    def add_control_delete(self, title, href):
       

        self.add_control(
            "storage:delete",
            href,
            method="DELETE",
            title=title,
        )

class InventoryBuilder(MasonBuilder):

    def add_control_all_products(self):
        self.add_control(
            "storage:products-all",
            api.url_for(ProductCollection)
        )

    def add_control_delete_product(self, product, handle):
        self.add_control_delete(
            "Delete this Product",
            api.url_for(ProductItem, product=product)
        )

    def add_control_add_product(self):
        self.add_control_post(
            "storage:add-product",
            "Add a new product",
            api.url_for(ProductCollection),
            Product.json_schema()
        )

    def add_control_edit_product(self, product, handle):
        self.add_control_put(
            "edit",
            api.url_for(ProductItem, product=product),
            Product.json_schema()
        )



api.add_resource(ProductCollection, "/api/products/")
app.url_map.converters["product"] = ProductConverter
api.add_resource(ProductItem, "/api/products/<product:product>/")


@app.route("/profiles/<resource>/")
def send_profile_html(resource):
    return "pass"


@app.route("/musicmeta/link-relations/")
def send_link_relations_html():
    return "here be link relations"
