import flask
from flask import request, jsonify, send_file
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import traceback

from DataCache import DataCache
from DatabaseRequester import DatabaseRequester
from TwitterAPIManager import TwitterAPIManager
from AlgorithmsManager import AlgorithmsManager
from TemporalDataManager import TemporalDataManager
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

# SETUP TemporalDataManager
# pass in algorithmsManager object and array of Location objects
timedata = TemporalDataManager(algo)

######################
# SETUP FLASK
# Below are FLASK Endpoints
app = flask.Flask(__name__)
# app.config["DEBUG"] = True
CORS(app)

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@app.route('/', methods=['GET'])
def home():
    return "<h1>HELLO</h1>" \
           "<br>Endpoints:<br>[/toptrends]<br>[/toptweets]<br>[/getlocation]<b>[/locations]<br>[/temporal]<br>[/trend_news]"


@app.route('/toptweets', methods=['GET'])
def api_toptweets():
    query = request.args.get('query')
    fromstr = request.args.get('from')
    tostr = request.args.get('to')
    num = request.args.get('num')
    sort = request.args.get('sort')
    latitude = request.args.get('latitude') or request.args.get('lat')
    longitude = request.args.get('longitude') or request.args.get('lon')

    try:
        print("/toptweets args: ", query, fromstr, tostr, num, sort, latitude, longitude)
        if query is not None:
            querystr = "/toptweets{}{}-{}".format(query, latitude, longitude)
            # default optional args values
            numint = 10
            fromdate = datetime.now() - timedelta(days=5)
            todate = datetime.now()
            issort = 1
            location = None

            # attempt to get optional args values
            if num is not None and int(num) > 0:
                numint = int(num)
            if fromstr is not None:  # try parsing the fromdate argument
                try:
                    fromdate = datetime.strptime(fromstr, '%Y-%m-%d')
                except ValueError as e:
                    print(type(e))
                    print(e.args)
                    print(e)
                    traceback.print_exc()
            if tostr is not None:   # try parsing the todate argument
                try:
                    todate = datetime.strptime(tostr, '%Y-%m-%d')
                except ValueError as e:
                    print(type(e))
                    print(e.args)
                    print(e)
                    traceback.print_exc()
            if sort is not None and (int(sort) == 0 or int(sort) == 1):
                issort = int(sort)
            if latitude is not None and longitude is not None:
                location = algo.get_location_by_latlon(float(latitude), float(longitude))

            print("\n/toptweets args: ", query, numint, latitude, longitude, fromdate, todate, issort, "\n")

            result = algo.get_top_tweets_from_query(query=query,
                                                    num=numint,
                                                    location=location,
                                                    timefrom=fromdate,
                                                    timeto=todate,
                                                    sort=issort,
                                                    querystr=querystr)

            return jsonify(result)  # result for this endpoint is not json format
        else:
            argstr = AlgorithmsManager.get_args_as_html_str(['query'],
                                            ['from', 'to', 'num', 'lat/latitude', 'lon/longitude', 'sort'])
            return "Error! arguments:<br><br>" + argstr
    except Exception as e:
        errStr = str(e)
        print("ERROR ENDPOINT /toptweets")
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return "ERROR ENDPOINT " + errStr


@app.route('/toptrends', methods=['GET'])
def api_toptrends():
    woeid = request.args.get('woeid')
    latitude = request.args.get('latitude') or request.args.get('lat')
    longitude = request.args.get('longitude') or request.args.get('lon')
    num = request.args.get('num')
    sort = request.args.get('sort')

    try:
        print("/toptrends args: ", woeid, latitude, longitude, num, sort)
        # TODO fix error here
        if woeid is None and (latitude is not None and longitude is not None):
            woeid = str(algo.get_location_by_latlon(float(latitude), float(longitude)).woeid)

        print(woeid)
        if woeid is not None:

            querystr = "/toptrends{}".format(woeid)

            numint = 5  # default val
            issort = 1  # default to yes sort

            # attempt to update value
            if num is not None and int(num) > 0:
                numint = int(num)
            if sort is not None and (int(sort) == 0 or int(sort) == 1):
                issort = int(sort)

            print("\n/toptrends args: ", woeid, latitude, longitude, numint, issort, "\n")

            result = algo.get_top_num_trends_from_location(woeid=int(woeid),
                                                           num=numint,
                                                           sort=issort,
                                                           querystr=querystr)
            return jsonify(result)   # result for this endpoint is not json format
        else:
            argstr = AlgorithmsManager.get_args_as_html_str(['[woeid]  <b>OR</b>   [lat <b>AND</b> lon]'], ['num', 'sort'])
            return 'Error! arguments:<br><br>' + argstr
    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /toptrends')
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr

@app.route('/getlocation', methods=['GET'])
def api_getlocation():
    address = request.args.get('address')
    latitude = request.args.get('latitude') or request.args.get('lat')
    longitude = request.args.get('longitude') or request.args.get('lon')
    woeid = request.args.get('woeid')

    try:
        print("\n/getlocation args: ", address, latitude, longitude, woeid, "\n")

        if address is not None:
            return jsonify(algo.get_location_by_address(address).__dict__)

        if latitude is not None and longitude is not None:
            lat = float(latitude)
            lon = float(longitude)
            return jsonify(algo.get_location_by_latlon(lat, lon).__dict__)

        if woeid is not None:
            return jsonify(algo.get_location_by_woeid(woeid).__dict__)

        argstr = AlgorithmsManager.get_args_as_html_str(['<b>Must have at least 1 of the three arguments</b>',
                                                        'address', 'latitude and longitude', 'woeid'], [])

        return 'Error! arguments:<br><br>' + argstr
    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /getlocation')
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr

@app.route('/locations', methods=['GET'])
def api_get_all_locations():
    print("/locations")
    return jsonify(algo.get_all_locations())

@app.route('/trend_news', methods=['GET'])
def api_get_trend_news():
    trend = request.args.get("trend")
    num_stories = request.args.get("num_stories")

    try:
        print("/trend_news args: ", trend, num_stories)
        if num_stories is None:
            result = algo.get_trend_news(trend=trend)
        else:
            result = algo.get_trend_news(trend=trend, num_stories=num_stories)
        result_json = jsonify(result)
    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /trend_news')
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr
    return result_json

# TODO: endpoint that returns the CSV file of trends and their temporal data
@app.route('/temporal', methods=['GET'])
def api_get_trends_snapshot():
    trends = request.args.get("trends")
    fromdate = request.args.get("from")     #YYYY-mm-dd HH:MM:SS
    todate = request.args.get("to")         #YYYY-mm-dd HH:MM:SS
    loc = request.args.get("woeid")         #optional woeid argument

    # args for the time step of each datapoint
    day = request.args.get("days")
    hour = request.args.get("hours")
    minutesString = request.args.get("minutes")
    sec = request.args.get("seconds")

    try:
        print("/temporal args: ", trends, fromdate, todate, loc, day, hour, minutesString, sec)

        if trends is not None:
            trendsparsed = trends.split(",")
            until = datetime.now()
            since = until - timedelta(hours=12)
            woeid = 1
            days = 0
            hours = 3
            minutes = 30
            seconds = 0

            try:
                if fromdate is not None:
                    since = datetime.strptime(fromdate, DATETIME_FORMAT)
                if todate is not None:
                    until = datetime.strptime(todate, DATETIME_FORMAT)
                # Final check to make sure since and until datetimes are valid
                if since >= until:
                    since = until - timedelta(hours=12)
            except Exception as e:
                print("/temporal -- datetimes not in the proper format of YYYY-mm-dd HH-MM-SS -- using default datetime")
                print("Exception: ", e.__doc__, str(e))
                traceback.print_exc()

            if loc is not None:
                try:
                    woeid = int(loc)
                except Exception as e:
                    print("/temporal -- invalid woeid -- using default woeid")
                    print("Exception: ", e.__doc__, str(e))
                    traceback.print_exc()

            if day is not None:
                try:
                    days = int(day)
                except Exception as e:
                    print("/temporal -- invalid day -- using default day")
                    print("Exception: ", e.__doc__, str(e))
                    traceback.print_exc()
            if hour is not None:
                try:
                    hours = int(hour)
                except Exception as e:
                    print("/temporal -- invalid hour -- using default hour")
                    print("Exception: ", e.__doc__, str(e))
                    traceback.print_exc()
            if minutesString is not None:
                try:
                    minutes = int(minutesString)
                except Exception as e:
                    print("/temporal -- invalid minute -- using default minute")
                    print("Exception: ", e.__doc__, str(e))
                    traceback.print_exc()
            if sec is not None:
                try:
                    seconds = int(sec)
                except Exception as e:
                    print("/temporal -- invalid second -- using default second")
                    print("Exception: ", e.__doc__, str(e))
                    traceback.print_exc()

            if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
                hours = 3
                minutes = 30

            csv = timedata.get_trends_snapshot_as_csv(trendsparsed, since, until, max(1, woeid), days, hours, minutes, seconds)
            return csv
        else:
            argstr = AlgorithmsManager.get_args_as_html_str(['trends'],
                                                            ['woeid', 'from', 'to'])
            return 'Error! arguments:<br><br>' + argstr
    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /temporal')
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr

    #todo cut unreachable code?
    return str(trendsparsed)

@app.route('/temporal_options', methods=['GET'])
def api_get_trends_history_summary():
    fromDateArg = request.args.get("from")  # YYYY-mm-dd HH:MM:SS
    toDateArg = request.args.get("to")  # YYYY-mm-dd HH:MM:SS
    locArg = request.args.get("woeid")  # optional woeid argument

    endDate = datetime.now()
    startDate = endDate- timedelta(hours=12)
    locId = None

    try:
        print("/temporal_options args: ", fromDateArg, toDateArg, locArg)

        try:
            if fromDateArg is not None:
                startDate = datetime.strptime(fromDateArg, DATETIME_FORMAT)
            if toDateArg is not None:
                endDate = datetime.strptime(toDateArg, DATETIME_FORMAT)
            # Final check to make sure since and until datetimes are valid
            if startDate >= endDate:
                print("/temporal_options -- datetimes not in valid order -- using default start and end dates")
                endDate = datetime.now()
                startDate = endDate - timedelta(hours=12)
        except Exception as e:
            print("/temporal_options -- datetimes not in the proper format of YYYY-mm-dd HH-MM-SS -- using default start and end dates")
            print("Exception: ", e.__doc__, str(e))
            traceback.print_exc()

        if locArg is not None:
            try:
                locId = int(locArg)
            except Exception as e:
                print("/temporal_options -- invalid location woeid -- fetching from all locations")
                print("Exception: ", e.__doc__, str(e))
                traceback.print_exc()

        trendsHistoryOptions = timedata.collect_trend_history_options(startDate, endDate, locId)
        return jsonify(trendsHistoryOptions)

    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /temporal_options')
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr




@app.route('/economics', methods=['GET'])
def api_get_economic_data():
    state = request.args.get('state')
    city = request.args.get('city')
    woeid = request.args.get('woeid')

    try:
        print("\n/economics args: ", state, city, woeid, "\n")

        if city is not None:
            return jsonify(algo.get_economic_data_by_city(city))

        if woeid is not None:
            return jsonify(algo.get_economic_data_by_woeid(woeid))

        if state is not None:
            return jsonify(algo.get_economic_data_by_state(state))

        argstr = AlgorithmsManager.get_args_as_html_str(['<b>Must have at least 1 of the three arguments</b>',
                                                        'state', 'city', 'woeid'], [])

        return 'Error! arguments:<br><br>' + argstr
    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /economics')
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr

@app.route('/wordcloud', methods=['GET'])
def api_get_wordcloud():
    #testID = 942781891714932738
    #username = "KisukiTsuo"

    userid = request.args.get('id')
    username = request.args.get('username')
    countstr = request.args.get('count')
    depthstr = request.args.get('depth')
    networkType = request.args.get('networkType')

    id2 = 0
    count = 20
    depth = 1
    try:
        if userid is not None:
            id2 = int(userid)
        if countstr is not None:
            count = int(countstr)
        if depthstr is not None:
            depth = int(depthstr)

        if networkType != AlgorithmsManager.FOLLOWER_NETWORK_TYPE and networkType != AlgorithmsManager.FRIEND_NETWORK_TYPE:
            raise ValueError("Invalid network type " + networkType)

    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /wordcloud')
        print('Exception: ', e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr

    print("\n/wordcloud args: ", id2, username, count, depth, networkType, "\n")

    wordcloudpath = algo.create_wordcloud_image(networkType, id2, username, count, depth)
    if wordcloudpath is None:
        return "Invalid user id or screen name"
    return send_file(wordcloudpath, mimetype='image/png')

@app.route('/user', methods=['GET'])
def api_get_twitter_user():
    username = request.args.get('username')

    try:
        if username is not None:
            
            user = algo.get_user_by_username(username)

            if user is not None:
                return jsonify(user)
            else:
                return "ERROR: Validation fails"

        argstr = AlgorithmsManager.get_args_as_html_str(['<b>Must have username'], [])

        return 'Error! arguments:<br><br>' + argstr

    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /user')
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr

# TODO: handling exceptions: RateLimitError, user has no retweeters
@app.route('/retweeters', methods=['GET'])
def api_get_most_frequent_retweeters():
    username = request.args.get('username')
    count = request.args.get('count')

    try:
        print("\n/retweeters args: ", username, count, "\n")

        if username is None and count is not None:
            #error msg: lack arg "username"
            argstr = AlgorithmsManager.get_args_as_html_str(['<b>Must have username'], [])
            return 'Error! arguments:<br><br>' + argstr

        if count is None and username is not None:
            #error msg: lack arg "count"
            argstr = AlgorithmsManager.get_args_as_html_str(['<b>Must have count parameter'], [])
            return 'Error! arguments:<br><br>' + argstr

        # Default: search through 20 most recent tweets and 20 retweeters per tweet
        # The server goes through these default parameters or the availability limit, whichever is smaller

        if username is not None and int(count) > 0:

            num = int(count)
            # Serious EXCEPTION: when the given user has no tweeters => return object type
            retweeters_dict = algo.get_most_frequent_retweeters(username, num_tweets=20, num_retweets=20)
            max_len = len(retweeters_dict)

            if num < max_len:
                #return the sorted short list
                shortList = algo.list_top_retweeters(retweeters_dict, num)
                print(shortList)
                return jsonify(shortList)

            if num >= max_len:
                #return the entire sorted list
                sortedList = algo.list_top_retweeters(retweeters_dict, max_len)
                print(sortedList)
                return jsonify(sortedList)
        
        if username is not None and int(count) == 0:

            argstr = AlgorithmsManager.get_args_as_html_str(['<b>count parameter must be larger than zero'], [])
            return 'Error! arguments:<br><br>' + argstr

        argstr = AlgorithmsManager.get_args_as_html_str(['<b>Must have two arguments</b>',
                                                        'username', 'count'], [])

        return 'Error! arguments:<br><br>' + argstr

    except Exception as e:
        errStr = str(e)
        print('ERROR ENDPOINT /retweeters')
        print("Exception: ", e.__doc__, errStr)
        traceback.print_exc()
        return 'ERROR ENDPOINT ' + errStr

@app.route('/test', methods=['GET'])
def api_test():
    #query = db.query("insert into trends_snapshot(id, woe_id, trend_content, query_term, tweet_volume, is_hashtag, created_date) "
    #                 "values(0, 1, 'test', 'testtest', 420, false, '2003-01-01 05:32:21.32');")
    #query = db.query(
    #    "insert into trends_snapshot(id, woe_id, trend_content, query_term, tweet_volume, is_hashtag, created_date) "
    #    "values(1, 1, 'test', 'testtest', 420, false, '2003-01-01 05:32:21.32');")

    #querystr = "insert into trends_snapshot(id, woe_id, trend_content, query_term, tweet_volume, is_hashtag, created_date) values(3, 2459115, '#COVID2019', '%%23COVID2019', 0, True, '2020-03-26 02:08:16.850816');"
    #query = db.query(querystr)
    #query = db.query("SELECT * FROM trends_snapshot;")
    #print(query.get_rows())
    #db.query("DELETE FROM trends_snapshot;")
    #csv = timedata.get_trends_snapshot_as_csv(['a', 'adad'], datetime.now()-timedelta(hours=12), datetime.now())
    # query = db.query("SELECT * FROM trends_snapshot;")
    #print(query.get_rows())

    #return csv
    testID = 942781891714932738
    username = "KisukiTsuo"
    tweets_str = algo.get_network_tweets_text(testID, username)
    return tweets_str


# dont use this endpoint too outdated. kept for reference.
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
if __name__ == "__main__":
    app.run()
