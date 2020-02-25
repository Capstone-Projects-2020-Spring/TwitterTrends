import flask
from flask import request, jsonify

from DataCache import DataCache
from DatabaseRequester import DatabaseRequester
from TwitterAPIManager import TwitterAPIManager
from AlgorithmsManager import AlgorithmsManager
import DataStructures


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
    if cache.should_update("users", 1):
        result = db.query("SELECT * FROM test_users;")
        users = []
        for row in result.get_rows():
            users.append({"id": row[0], "email": row[1]})
        json = jsonify(users)
        cache.add("users", json, 1)
        return json
    else:
        print("Returning USERS results from cache")
        return cache.retrieve("users")


@app.route('/tweets', methods=['GET'])
def api_ttweets():
    if cache.should_update("tweets", 1):
        result = db.query("SELECT * FROM test_tweets;")
        tweets = []
        for row in result.get_rows():
            tweets.append(DataStructures.Tweet(row[0], row[1], row[2], row[3]).__dict__)
        json = jsonify(tweets)
        cache.add("tweets", json, 1)
        return json
    else:
        print("Returning TWEETS results from cache")
        return cache.retrieve("tweets")


@app.route('/test', methods=['GET'])
def api_test():
    return jsonify(["Test", "Test2"])


@app.route('/testcd', methods=['GET'])
def api_testcd():
    result = db.query("SELECT * FROM test_conor_dan;");
    return jsonify(result)


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
