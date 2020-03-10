import flask
from flask import request, jsonify
from datetime import datetime

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
algo = AlgorithmsManager(cache, db, twitter)


######################
# SETUP FLASK
# Below are FLASK Endpoints
app = flask.Flask(__name__)
app.config["DEBUG"] = True

################
# TODO: add proper end points. Most endpoints are currently broken
################

@app.route('/', methods=['GET'])
def home():
    return "<h1>HELLO</h1>" \
           "<br>Endpoints:<br>[/test]<br>[/toptrends]"


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


@app.route('/toptrends', methods=['GET'])
def api_toptrends():
    woeid = request.args.get('woeid')
    latitude = request.args.get('latitude') or request.args.get('lat')
    longitude = request.args.get('longitude') or request.args.get('lon')
    num = request.args.get('num')

    try:
        if woeid is not None:
            numint = 5
            if num is not None and int(num) > 0:
                numint = int(num)

            print("\n/toptrends args: ", woeid, latitude, longitude, numint, "\n")

            result = algo.get_top_num_trends_from_location(int(woeid), numint, querystr="/toptrends"+woeid)
            return result # result is in json format
        else:
            argstr = AlgorithmsManager.get_args_as_html_str(["woeid"], ["num"])
            return "Error! arguments:<br><br>" + argstr
    except:
        print("ERROR ENDPOINT /toptrends")
        return "ERROR ENDPOINT"

@app.route('/toptrends2', methods=['GET'])
def api_toptrends2():
    if cache.should_update("toptrends", 1):
        result = algo.get_top_5_trends_from_zip_code("19148")  # db.query("SELECT * FROM test_tweets;")
        json = jsonify(result)
        cache.add("toptrends", json, 1)
        return json
    else:
        print("Returning TOP 5 TRENDS results from cache")
        return cache.retrieve("toptrends")


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
