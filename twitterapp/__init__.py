from flask import Flask

app = Flask(__name__)


from twitterapp import routes
