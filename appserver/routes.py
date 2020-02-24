from flask import render_template
from twitterapp import app


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/trend")
def trend():
    return render_template('trend.html')


@app.route("/user")
def user():
    return render_template('user.html')



@app.route("/login")
def login():
    return render_template('login.html')

