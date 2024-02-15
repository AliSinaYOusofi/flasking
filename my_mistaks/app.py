from flask import Flask, render_template, g, redirect, session
from flask import request
from database.db import connect_to_sqlite
import datetime
import sqlite3
from utils.hash_password import hash_password
from utils.match_passwords import match_passwords
from flask_json import FlaskJSON, JsonError, json_response, as_json
import secrets
import uuid

app = Flask(__name__)
json = FlaskJSON(app) # using json

json.init_app(app) # starting json

app.secret_key = secrets.token_hex()
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
    
    front_from_data = request.json

    email = front_from_data['email']
    password = front_from_data['password']
    
    query = 'SELECT * FROM users WHERE email = ?'
    sqlite_conn = get_db()
    
    cursor = sqlite_conn.cursor()
    
    try:
        
        sql_obj = cursor.execute(query, (email,))
        
        result = sql_obj.fetchone()
        
        if not result: return json_response(message="User not found")
        
        fetched_password = result[3]
        
        if not match_passwords(password, fetched_password):
            return json_response(message="emailOrPasswordIncorrect")
        
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        return json_response(message="success", session_id=session_id)
    except sqlite3.Error as e:
    
        print(e, 'error bro')
        return json_response(message="error")


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
    
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id

    return redirect("/main")

@app.route("/main")
def user_homepage():
    return render_template("main.html")