import flask
from flask import request, jsonify

from DataCache import DataCache
from DatabaseRequester import DatabaseRequester
from TwitterAPIManager import TwitterAPIManager
from AlgorithmsManager import AlgorithmsManager

# SETUP DataCache
cache = DataCache()

# SETUP DatabaseRequester
db = DatabaseRequester( host="twittertrends.cmxd9oibzmhi.us-east-2.rds.amazonaws.com",
                        port="5432",
                        database="postgres",
                        user="master_user",
                        password="ULllhejK2ykYroghntj0"
)

# SETUP TwitterAPIManager
twitter = TwitterAPIManager()

# SETUP AlgorithmsManager
algo = AlgorithmsManager()


######################
# SETUP FLASK
# Below are FLASK Endpoints
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>HELLO MIKE</h1><p>I am saying hi to mike</p>" \
           "<br>Endpoints:<br>[/test]<br>[/users]<br>[/tweets]"


@app.route('/users', methods=['GET'])
def api_tusers():
    result = db.query("SELECT * FROM test_users;")
    return jsonify(result)


@app.route('/tweets', methods=['GET'])
def api_ttweets():
    result = db.query("SELECT * FROM test_tweets;")
    return jsonify(result)


@app.route('/test', methods=['GET'])
def api_test():
    return jsonify(["Test", "Test2"])


@app.route('/testadd', methods=['GET'])
def api_testadd():
    db.query("DELETE FROM test_users WHERE id = 13;")
    result = db.query(  "INSERT INTO test_users "
                        "VALUES (13, \'dantest3@test.com\');")
    return jsonify(result) # "Test Add Endpoint" #jsonify(result)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# Run the Flask server
app.run()
