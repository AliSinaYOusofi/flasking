from flask import Flask, render_template

from flask import request


app = Flask(__name__)



@app.route("/")

def home():

    return render_template("home.html")


@app.route("/login")

def login_form():

    return render_template("login.html")


@app.route("/auth/login", methods=["POST"])

def auth_login():
    
    email = request.form["email"]

    password = request.form["password"]
    
    print(email, password, 'username and password')
    if email == "admin" and password == "admin":

        return "<h1> Okay </h1>"

    else:

        return "<h1> Not Okay </h1>"

    return "<h1> Okay </h1>"