from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound, BadRequest
from jsonschema import validate, ValidationError
from datetime import datetime
from rfc3339_validator import validate_rfc3339

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    altitude = db.Column(db.Float, nullable=True)
    description=db.Column(db.String(256), nullable=True)
    
    sensor = db.relationship("Sensor", back_populates="location", uselist=False)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    model = db.Column(db.String(128), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id", ondelete="SET NULL"))
    
    location = db.relationship("Location", back_populates="sensor")
    measurements = db.relationship("Measurement", back_populates="sensor")

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id", ondelete="SET NULL"))
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    
    sensor = db.relationship("Sensor", back_populates="measurements")

    def deserialize(self, doc):
        self.value = doc["value"]
        self.time = datetime.fromisoformat(doc["time"])

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["value", "time"]
        }
        props = schema["properties"] = {}
        props["value"] = {
            "description": "value",
            "type": "number"
        }
        props["time"] = {
            "description": "time",
            "type": "string",
            "format": "date-time"
        }
        return schema

class SensorCollection(Resource):
    def get(self):
        sensors = Sensor.query.all()
        res = []
        for sensor in sensors:
            res.append({ "name": sensor.name })
        return res, 200

class MeasurementCollection(Resource):
    def post(self, sensor):
        print(request.json)
        if not request.json:
            Response(status=415)
        try:
            validate(request.json, Measurement.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error))
        if request.json["time"] is None:
            raise BadRequest(description="time field is required")
        if not validate_rfc3339(request.json["time"]):
            raise BadRequest(description="time validation error")

        measurement = Measurement()
        measurement.deserialize(request.json)
        measurement.sensor = sensor
        print(type(measurement.time))
        print(f"{measurement.sensor.name}, {measurement.value}, {measurement.time}")
        db.session.add(measurement)
        db.session.commit()
        print(measurement.id)
        response = Response()
        response.status = 201
        response.headers['Location'] = f'/api/sensors/{sensor.name}/measurements/{measurement.id}/'
        response.headers['Content-Type'] = "text/html"
        return response

class SensorConverter(BaseConverter):
    def to_python(self, name):
        db_model = Sensor.query.filter_by(name=name).first()
        if db_model is None:
            raise NotFound
        return db_model
        
    def to_url(self, db_model):
        return db_model.name

app.url_map.converters["sensor"] = SensorConverter
api.add_resource(SensorCollection, "/api/sensors/")
api.add_resource(MeasurementCollection, "/api/sensors/<sensor:sensor>/measurements/")
