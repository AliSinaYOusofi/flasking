from flask import Flask, render_template, g
from flask import request
from database.db import connect_to_sqlite
import datetime
import sqlite3

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_sqlite()
    return db

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
    
    if email == "admin" and password == "admin":

        return "<h1> Okay </h1>"

    else:

        return "<h1> Not Okay </h1>"

    return "<h1> Okay </h1>"

@app.route("/signup", methods=["POST"])
def signup():
    
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    joining_date = datetime.datetime.now()
    
    query = 'INSERT INTO users (name, email, joining_date, password) VALUES (?, ?, ?, ?)'
    
    sqlite_conn = get_db()
    
    # sqlite_conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, joining_date DATETIME, password TEXT)')
    try:
        sqlite_conn.execute(query, (username, email, joining_date, password))
        sqlite_conn.commit()
    except sqlite3.Error as e:
        print(e, 'error bro')
        return "<h1> Error </h1>"
    return "<h1> Your are now registered </h1>"