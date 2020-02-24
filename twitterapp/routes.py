from flask import render_template
from twitterapp import app

@app.route("/")
def home():
    return 'Home Page of Twitter Trends'
