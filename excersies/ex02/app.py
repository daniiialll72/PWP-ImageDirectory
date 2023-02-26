import json
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

deployments = db.Table("deployments",
    db.Column("deployment_id", db.Integer, db.ForeignKey("deployment.id"), primary_key=True),
    db.Column("sensor_id", db.Integer, db.ForeignKey("sensor.id"), primary_key=True)
)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    altitude = db.Column(db.Float, nullable=True)
    description=db.Column(db.String(256), nullable=True)
    
    sensor = db.relationship("Sensor", back_populates="location", uselist=False)

class Deployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    
    sensors = db.relationship("Sensor", secondary=deployments, back_populates="deployments")

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    model = db.Column(db.String(128), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), unique=True)
    
    location = db.relationship("Location", back_populates="sensor")
    measurements = db.relationship("Measurement", back_populates="sensor")
    deployments = db.relationship("Deployment", secondary=deployments, back_populates="sensors")
    
class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id", ondelete="SET NULL"))
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
        
    sensor = db.relationship("Sensor", back_populates="measurements")


class SensorCollection(Resource):
    def get(self):
        pass
    def post(self):
        pass

class SensorItem(Resource):
    def get(self, sensor):
        pass
    def put(self, sensor):
        pass
    def delete(self, sensor):
        pass

@app.route("/<sensor_name>/measurements/add/", methods=["POST"])
def add_measurement(sensor_name):
    # This branch happens when user submits the form
    try:
        sensor = Sensor.query.filter_by(name=sensor_name).first()
        if sensor:
            value = float(request.json["value"])
            meas = Measurement(
                sensor=sensor,
                value=value,
                time=datetime.now()
            )
            db.session.add(meas)
            db.session.commit()
            return "", 201
        else:
            abort(404)
    except (KeyError, ValueError, IntegrityError):
        abort(400)

@app.route("/sensors/")
def get_sensors():
    response_data = []
    sensors = Sensor.query.all()
    for sensor in sensors:
        response_data.append([sensor.name, sensor.model])        
    return json.dumps(response_data)

def post(self):
    if not request.json:
        abort(415)
            
    try:
        sensor = Sensor(
            name=request.json["name"],
            model=request.json["model"],
        )
        db.session.add(sensor)
        db.session.commit()
    except KeyError:
        abort(400)
    except IntegrityError:
        abort(409)
    return "", 201

api.add_resource(SensorCollection, "/api/sensors/")
api.add_resource(SensorItem, "/api/sensors/<sensor>/")
