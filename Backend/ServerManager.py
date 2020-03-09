import flask
from flask import request, jsonify
from datetime import datetime

from DataCache import DataCache
from DatabaseRequester import DatabaseRequester
from TwitterAPIManager import TwitterAPIManager
from AlgorithmsManager import AlgorithmsManager
import DataStructures

import os
import tweepy

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

apikey = os.environ.get("TWITTER_TRENDS_API_KEY")
print(apikey)
apisecretkey = os.environ.get("TWITTER_TRENDS_API_SECRET_KEY")
print(apisecretkey)
apitoken = os.environ.get("TWITTER_TRENDS_ACCESS_TOKEN")
print(apitoken)
apitokensecret = os.environ.get("TWITTER_TRENDS_ACCESS_TOKEN_SECRET")
print(apitokensecret)
acctype = os.environ.get("SEARCHTWEETS_ACCOUNT_TYPE")
print(acctype)
accconsumer = os.environ.get("SEARCHTWEETS_CONSUMER_KEY")
print(accconsumer)
accconsumersecret = os.environ.get("SEARCHTWEETS_CONSUMER_SECRET")
print(accconsumersecret)

auth = tweepy.OAuthHandler(apikey, apisecretkey)
auth.set_access_token(apitoken, apitokensecret)

api = tweepy.API(auth)

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


@app.route('/trends', methods=['GET'])
def api_trends():
    result = db.query("SELECT * FROM Trend;")
    return jsonify(result)


@app.route('/toptrends', methods=['GET'])
def api_toptrends():
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
    try:
        api.verify_credentials()
        print("Valid credentials")

        woeid = 2379574
        query = api.trends_place(woeid)
        print(query)

        queryObj = query[0]
        as_of = queryObj['as_of']
        created_at = queryObj['created_at']
        loc_name = queryObj['locations'][0]['name']
        loc_woeid = queryObj['locations'][0]['woeid']

        print(as_of, created_at, loc_name, loc_woeid)

        trends = []
        i = 0
        for trend in queryObj['trends']:
            pk = trend['tweet_volume']
            trends.append(DataStructures.Trend(pk if pk is not None else 0,
                                               trend['name'],
                                               True if trend['name'][0] == '#' else False,
                                               trend['query']))
            i += 1

        # print(trends[0].trend_PK)
        trends_5 = []
        length = len(trends)
        for l in range(length):
            if l+1 < length:
                temp = trends[l+1]
                j = l
                for k in range(len(trends)):
                    j = l - k
                    if j >= 0 and temp.trend_PK < trends[j].trend_PK:
                        trends[j + 1] = trends[j]
                    else:
                        break
                trends[j + 1] = temp
            else:
                break
        for trend in trends:
            trends_5.append(trend.__dict__)

        return jsonify(trends_5)
    except:
        print("Tweepy unable to authenticate")
    #return jsonify(["Test", "Test2"])


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
