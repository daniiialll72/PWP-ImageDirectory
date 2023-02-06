# Group work: Nazanin Nakhaie Ahooie, Mehrdad Kaheh, Sepehr Samadi, Danial Khaledi
import math
from flask import Flask, request

app = Flask("main")
@app.route("/trig/<func>/")
def trig(func):
    try:
        angle = float(request.args["angle"])
    except KeyError:
        return "Missing query parameter: angle", 400
    except ValueError:
        return "Invalid query parameter(angle) value(s)", 400

    unit = request.args.get("unit")
    print(unit)
    if unit is not None:
        if unit not in ["radian", "degree"]:
            return "Invalid query parameter(radian or degree)", 400 

        if unit == "degree":
            angle = math.radians(angle)
        elif unit == "radian":
            angle = angle

    if func == "sin":
        result = math.sin(angle)
    elif func == "cos":
        result = math.cos(angle)
    elif func == "tan":
        result = math.tan(angle)

    else: 
        return "operation not found", 404
    return str(round(result,3)), 200

