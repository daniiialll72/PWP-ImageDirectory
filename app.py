# Group work: Nazanin Nakhaie Ahooie, Mehrdad Kaheh, Sepehr Samadi, Danial Khaledi
from flask import Flask

app = Flask("main")

@app.route("/")
def index():
    return "how to use: Use the calculator to Add, Substract, Devide and multiply."

@app.route("/add/<float:number_1>/<float:number_2>/")
def plus(number_1, number_2):
    string_representation = str(number_1 + number_2)
    return "the added result is:" + string_representation 

@app.route("/sub/<float:number_1>/<float:number_2>/")
def minus(number_1, number_2):
    string_representation = str(number_1 - number_2)
    return "the substracted result is:" + string_representation 

@app.route("/mul/<float:number_1>/<float:number_2>/")
def mult(number_1, number_2):
    string_representation = str(number_1 * number_2)
    return "the multiplied result is:" + string_representation

@app.route("/div/<float:number_1>/<float:number_2>/")
def div(number_1, number_2):
    if number_1 == 0.0 or number_2 == 0.0:
        return "NaN"
    string_representation = str(number_1 / number_2)
    return "the devided result is:" + string_representation
