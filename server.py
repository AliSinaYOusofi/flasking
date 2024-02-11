from flask import Flask, render_template, request, session, redirect, url_for, flash
from markupsafe import escape
from termcolor import colored
from Models.StockModel import StockModel
from pydantic import ValidationError
import secrets

app = Flask(__name__)
# So, you need a way to store user-specific data for non-authenticated users between requests

app.secret_key = secrets.token_hex()

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/homepage")
def welcome_homepage():
    return 'is the homepage'

@app.route("/about")
def about():
    return '<p> about page </p>'

@app.route("/another", methods=['GET', 'POST', "PATCH"])
def another():
    return 'another one'


#   By convention, a trailing slash at the end of a URL indicates that the URL is a folder or 
# a directory. In other words, when the list of stocks in a user's portfolio is displayed, 
# the /stocks/ route will be used. This approach indicates that you have routes for 
# individual stocks, like /stocks/1, /stocks/2, /stocks/57, and so forth.
@app.get("/get-this-bitch")
def get_this_bithc():
    return 'get it babe'


# onto variable routing
@app.get("/hello/<message>")
def hello_message(message):
    return f'<h1> welcome {escape(message)} </h1>'

## for adding type checking we can and the type before the variable url part
@app.get("/blog_posts/<int:post_id>")
def get_blog_posts(post_id):
    if post_id:
        return f'<h1> The id of the blog {escape(post_id)} </h1>'
    return '<h1> All of the blog posts </h1>'


## template literals and forms and validation with pydantic

@app.get("/variable-names/<var_name>")
def variable_names(var_name):
    return render_template('about.html', var_name=var_name)

@app.route("/add_stock", methods=["GET", "POST"])
def add_stock():
    
    print(colored(request.form, "green", "on_red"))
    
    if request.method == 'POST':
        
        for key, value in request.form.items():
        
            print(f'{key}: {value}')
        
        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(colored(stock_data, 'cyan', 'on_white'))
            ## saving the form inputs into the session obj
            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price
            
            return redirect(url_for("list_stocks"))
        except ValidationError as e:
            print(colored(e + ' error', 'red', 'on_black'))
    
    return render_template('add_stock.html')

@app.route("/stocks/")
def list_stocks():
    print(colored(session, "blue", "on_white"))
    flash("stocks we added", "info")
    return render_template('stocks.html')


## okay for flash messages

@app.route("/login_form")
def render_login_form():
    return render_template("long_form.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == 'GET':
        return "<h1> Login via form </h1>"
    if request.method == "POST":
        password = request.form['password']
        
        if (password == '123'):
            flash("You are logged in")
            return render_template("success.html")
        return redirect(url_for("render_login_form"))