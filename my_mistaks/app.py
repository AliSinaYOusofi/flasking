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

from flask import url_for

import jwt


app = Flask(__name__)

json = FlaskJSON(app) # using json


json.init_app(app) # starting json


app.secret_key = secrets.token_hex()
app.permanent_session_lifetime = 3600

def get_db():

    db = getattr(g, '_database', None)

    if db is None:

        db = g._database = connect_to_sqlite()

    return db


# setup middleware

@app.before_request

def check_session():
    
    to_be_checeed = ['/login', '/signup', '/main', '/posts', '/create_post', '/save_post', '/view_posts/']
    if request.path == '/login' or request.path == '/signup':
        return
    

    elif request.path in to_be_checeed:

        if 'session_id' not in session:

            return redirect(url_for('login_form'))



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
        

        jwt_session_id = jwt.encode({'email': email}, app.secret_key, algorithm='HS256')

        session['session_id'] = jwt_session_id
        

        return json_response(message="success", session_id=jwt_session_id)

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
    
    session_jwt_token = jwt.encode({'email': email}, app.secret_key, algorithm='HS256')

    session['session_id'] = session_jwt_token

    return redirect("/main")


@app.route("/main")

def user_homepage():

    return render_template("main.html")


@app.route("/create_post")

def create_post():

    return render_template("create_post.html")


@app.route("/save_post", methods=["POST"])

def create_post_save():

    post_content = request.json['content']

    jwt_session_id = session['session_id']
    
    jwt_decode_result = jwt.decode(jwt_session_id, app.secret_key, algorithms=['HS256'])
    
    query = 'INSERT INTO posts (post, author) VALUES (?, ?)'
    
    try:
        
        sqlite_conn = get_db()
        
        sqlite_cursor = sqlite_conn.cursor()
        
        
        query_result = sqlite_cursor.execute(query, (post_content, jwt_decode_result['email']))

        sqlite_conn.commit()
        sqlite_cursor.close()
        return json_response(message="Post saved")
    
    except sqlite3.Error as err:
        print(err)
        return json_response(message="Error")
    
@app.route("/view_posts/")
def view_posts():
    
    # if the post_id is present then we will fetch a single post
        
    sqlite_conn = get_db()
    cursor = sqlite_conn.cursor()
    
    try:
        
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()
        return render_template("posts.html", posts=posts)
    except sqlite3.Error as e:
        print(e, "Error Bro")
        return json_response(message="Error")
    
@app.route("/view_posts/<int:post_id>")
def view_post_based_on_id(post_id):
    
    print(post_id, ' post_id')
    
    if post_id:

        query = 'SELECT * FROM posts WHERE id = ?'

        sqlite_conn = get_db()

        cursor = sqlite_conn.cursor()

        try:

            cursor.execute(query, (post_id,))

            posts = cursor.fetchall()

            return render_template("view_post.html", posts=posts)

        except sqlite3.Error as e:
            print(e, "Error Bro")
            return json_response(message="Error")
        
@app.route("/logout")
def logout():
    if 'session_id' in session:
        session.pop('session_id')
        return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route("/profile")
def profile():
    pass