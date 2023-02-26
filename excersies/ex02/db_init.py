import importlib
import random
import os
flask_app = os.environ.get("FLASK_APP")
app = importlib.import_module(flask_app)

app.db.create_all()

for idx, letter in enumerate("ABC", start=1):
    loc = app.Location(
        name=f"Location-{letter}",
        latitude=round(random.random() * 100, 2),
        longitude=round(random.random() * 100, 2),
        altitude=round(random.random() * 100, 2),
    )
    sensor = app.Sensor(
        name=f"Sensor-{idx}",
        model="test-sensor",
    )
    sensor.location = loc
    app.db.session.add(sensor)
    
app.db.session.commit()
