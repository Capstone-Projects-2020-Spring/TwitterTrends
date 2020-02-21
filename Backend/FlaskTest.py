import psycopg2
import flask
from flask import request, jsonify

# for database
from DatabaseRequester import DatabaseRequester

app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

# setting up database requester object
db = DatabaseRequester( host="twittertrends.cmxd9oibzmhi.us-east-2.rds.amazonaws.com",
                        port="5432",
                        database="postgres",
                        user="master_user",
                        password="ULllhejK2ykYroghntj0")

@app.route('/', methods=['GET'])
def home():
    return "<h1>HELLO MIKE</h1><p>I am saying hi to mike</p>" \
           "<br>Endpoints:<br>[/test]<br>[/users]<br>[/tweets]"


@app.route('/users', methods=['GET'])
def api_dbusers():
    result = db.query("SELECT * FROM test_users;")
    return jsonify(result)


@app.route('/tweets', methods=['GET'])
def api_all():
    result = db.query("SELECT * FROM test_tweets;")
    return jsonify(result)


@app.route('/test', methods=['GET'])
def api_id():
    return jsonify(books)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()

