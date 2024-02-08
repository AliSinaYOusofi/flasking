from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

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