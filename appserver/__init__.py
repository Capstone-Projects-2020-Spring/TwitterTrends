from flask import Flask
from flask import render_template

app = Flask(__name__,static_url_path='',
         static_folder='website-bootstrap', template_folder='website-bootstrap')

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/location")
def location():
    return render_template('location.html')


@app.route("/network")
def network():
    return render_template('network.html')


@app.route("/time")
def time():
    return render_template('time.html')