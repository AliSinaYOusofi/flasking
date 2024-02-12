from flask import Flask, render_template, g, redirect
from flask import request
from database.db import connect_to_sqlite
import datetime
import sqlite3
from utils.hash_password import hash_password
from utils.match_passwords import match_passwords

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
    
    query = 'SELECT * FROM users WHERE email = ?'
    sqlite_conn = get_db()
    
    cursor = sqlite_conn.cursor()
    
    try:
        
        sql_obj = cursor.execute(query, (email,))
        
        result = sql_obj.fetchone()
        
        if not result: return "<h1> User not found </h1>"
        
        fetched_password = result[3]
        
        if not match_passwords(password, fetched_password):
            return "<h1> Password is not correct </h1>"
        return "<h1> Okay </h1>"
    
    except sqlite3.Error as e:
    
        print(e, 'error bro')
        return "<h1> Error BRO </h1>"

    return "<h1> Okay </h1>"

@app.route("/signup", methods=["POST"])
def signup():
    
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    bcrypted_password = hash_password(password)
    joining_date = datetime.datetime.now()
    
    query = 'INSERT INTO users (name, email, joining_date, password) VALUES (?, ?, ?, ?)'
    
    sqlite_conn = get_db()
    
    # sqlite_conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, joining_date DATETIME, password TEXT)')
    
    try:
        sqlite_conn.execute(query, (username, email, joining_date, bcrypted_password))
        sqlite_conn.commit()
    except sqlite3.Error as e:
        print(e, 'error bro')
        return "<h1> Error </h1>"
    return redirect("/main")

@app.route("/main")
def user_homepage():
    return render_template("main.html")