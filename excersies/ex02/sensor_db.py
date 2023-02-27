from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

ctx = app.app_context()
ctx.push()

# deployments = db.Table("deployments",
#     db.Column("deployment_id", db.Integer, db.ForeignKey("deployment.id"), primary_key=True),
#     db.Column("sensor_id", db.Integer, db.ForeignKey("sensor.id"), primary_key=True)
# )

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
    # deployments = db.relationship("Deployment", secondary=deployments, back_populates="sensors")

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id", ondelete="SET NULL"))
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    
    sensor = db.relationship("Sensor", back_populates="measurements")

db.create_all()

# # part 1 (change the parameters, add random numbers!)
loc_a = Location(latitude=12.98, longitude=77.58, altitude=990, description="First Location")
loc_b = Location(latitude=13.08, longitude=77.68, altitude=900, description="Second Location")

# # Q5, Part 2 (name o model ro Avaz konin, inja chefck konin bebinid chera measurement o baghie attribute-ha ro ezafe nakardim(nemikhast?!))
sensor_1 = Sensor(name="sensor_1", model="model_1", location=loc_a)
sensor_2 = Sensor(name="sensor_2", model="model_2", location=loc_b)

# # Q5, part4
db.session.add(loc_a)
db.session.add(loc_b)
db.session.add(sensor_1)
db.session.add(sensor_2)
db.session.commit()