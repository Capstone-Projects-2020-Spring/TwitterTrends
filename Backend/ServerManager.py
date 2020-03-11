import flask
from flask import request, jsonify
from datetime import datetime, timedelta

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
           "<br>Endpoints:<br>[/test]<br>[/toptrends]<br>[/toptweets]"


@app.route('/toptweets', methods=['GET'])
def api_toptweets():
    query = request.args.get('query')
    fromstr = request.args.get('from')
    tostr = request.args.get('to')
    num = request.args.get('num')
    sort = request.args.get('sort')

    try:
        if query is not None:
            querystr = "/toptweets" + query
            # default optional args values
            numint = 10
            fromdate = datetime.now() - timedelta(days=5)
            todate = datetime.now()
            issort = 1

            # attempt to get optional args values
            if num is not None and int(num) > 0:
                numint = int(num)
            if fromstr is not None:  # try parsing the fromdate argument
                try:
                    fromdate = datetime.strptime(fromstr, '%Y-%m-%dT%H:%M:%S')
                except ValueError as e:
                    print(type(e))
                    print(e.args)
                    print(e)
            if tostr is not None:   # try parsing the todate argument
                try:
                    todate = datetime.strptime(tostr, '%Y-%m-%dT%H:%M:%S')
                except ValueError as e:
                    print(type(e))
                    print(e.args)
                    print(e)
            if issort is not None and int(issort) == 0 or int(issort) == 1:
                issort = int(sort)

            print("\n/toptweets args: ", query, fromdate, todate, numint, issort, "\n")

            result = algo.get_top_tweets_from_query(query=query,
                                                    num=numint,
                                                    timefrom=fromdate,
                                                    timeto=todate,
                                                    sort=issort,
                                                    querystr=querystr)

            return jsonify(result)  # result for this endpoint is not json format
        else:
            argstr = AlgorithmsManager.get_args_as_html_str(['query'], ['fromdate', 'todate', 'num', 'sort'])
            return "Error! arguments:<br><br>" + argstr
    except:
        print("ERROR ENDPOINT /toptweets")
        return "ERROR ENDPOINT"


@app.route('/toptrends', methods=['GET'])
def api_toptrends():
    woeid = request.args.get('woeid')
    latitude = request.args.get('latitude') or request.args.get('lat')
    longitude = request.args.get('longitude') or request.args.get('lon')
    num = request.args.get('num')
    sort = request.args.get('sort')

    try:
        if woeid is not None:
            querystr = "/toptrends"+woeid
            numint = 5  # default val
            issort = 1  # default to yes sort

            # attempt to update value
            if num is not None and int(num) > 0:
                numint = int(num)
            if sort is not None and int(sort) == 0 or int(sort) == 1:
                issort = int(sort)

            print("\n/toptrends args: ", woeid, latitude, longitude, numint, issort, "\n")

            result = algo.get_top_num_trends_from_location(woeid=int(woeid),
                                                           num=numint,
                                                           sort=issort,
                                                           querystr=querystr)
            return jsonify(result)   # result for this endpoint is not json format
        else:
            argstr = AlgorithmsManager.get_args_as_html_str(['woeid'], ['num', 'sort'])
            return 'Error! arguments:<br><br>' + argstr
    except:
        print('ERROR ENDPOINT /toptrends')
        return 'ERROR ENDPOINT'


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
