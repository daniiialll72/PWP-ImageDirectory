# # part 1 (change the parameters, add random numbers!)
# loc_a = Location(latitude=12.98, longitude=77.58, altitude=990, description="First Location")
# loc_b = Location(latitude=13.08, longitude=77.68, altitude=900, description="Second Location")

# # Q5, Part 2 (name o model ro Avaz konin, inja chefck konin bebinid chera measurement o baghie attribute-ha ro ezafe nakardim(nemikhast?!))
# sensor_1 = Sensor(name="sensor_1", model="model_1", location=loc_a)
# sensor_2 = Sensor(name="sensor_2", model="model_2", location=loc_b)

# # Q5, part3
# deployment = Deployment(name="deployment")
# deployment.sensors.append(sensor_1)
# deployment.sensors.append(sensor_2)

# # Q5, part4
# db.session.add(loc_a)
# db.session.add(loc_b)
# db.session.add(sensor_1)
# db.session.add(sensor_2)
# db.session.add(deployment)
# db.session.commit()