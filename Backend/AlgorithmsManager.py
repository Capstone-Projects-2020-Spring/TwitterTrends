from datetime import datetime, timedelta
from wrappers.geocode import geocoding

# from flask import jsonify # pronbably not needed
import DataStructures

# In charge of all algorithms needed by the backend server


class AlgorithmsManager:

    def __init__(self, cache, db, twit):
        self.cache = cache
        self.database = db
        self.twitter = twit

    # use the woeid argument to pull trends from Twitter API
    # pull results from cache if query was called recently
    # return top [num] trends
    # querystr argument is used for cache checking
    #       querystr must not be None
    def get_top_num_trends_from_location(self, woeid, num, sort=1, querystr=None):

        if querystr is None:
            querystr = "/toptrends{}".format(woeid)

        cachetime = 5 # n minutes cache time check

        if self.cache.should_update(querystr, cachetime) or querystr is None:

            queryres = self.twitter.top_trends(woeid)  # api.trends_place(woeid)

            # Variables storing other info about the trends
            as_of = queryres['as_of']
            created_at = queryres['created_at']
            loc_name = queryres['locations'][0]['name']
            loc_woeid = queryres['locations'][0]['woeid']

            trends = []   # List of Trend objects
            i = 0
            for trend in queryres['trends']:
                vol = trend['tweet_volume']
                tempTrend = DataStructures.Trend(i,
                                                 trend['name'],
                                                 True if trend['name'][0] == '#' else False,
                                                 trend['query'],
                                                 vol)

                trends.append(tempTrend)
                i += 1

            # SORT the trends returned by the tweet volume
            # Sorting will ruin the true "local" trends.
            if sort == 1:
                print("SORTING TRENDS")
                AlgorithmsManager.sort_trends(trends)

            trends_n = []

            for k in range(0, min(num, len(trends))):
                trends_n.append(trends[k].__dict__)

            self.cache.add(querystr, trends, cachetime)
            return trends_n
        else:
            print("\nReturning [", querystr , "] from cache\n")
            trends = self.cache.retrieve(querystr)
            trends_n = []
            for k in range(0, min(num, len(trends))):
                trends_n.append(trends[k].__dict__)
            return trends_n
    # end get top trends from location

    # get a list of tweets from given query
    # return from cache if recently called
    # tweets time will be between timefrom->timeto
    # sort the list of tweets by retweet_count if sort == 1
    # return the number of tweets equal to specified num
    # optional Location object can be passed in
    # querystr is used for caching
    def get_top_tweets_from_query(self, query, num, location,
                                timefrom=datetime.now() - timedelta(days=5),
                                timeto=datetime.now(),
                                sort=1, querystr=None):
        # Call a function from the TwitterAPIManager to return a list of tweets
        if querystr is None:
            querystr = "/toptweets{}{}-{}".format(query, location.latitude, location.longitude)

        cachetime = 15 # n minutes cache time check

        if self.cache.should_update(querystr, cachetime):

            # apitype 0 = standard 7 days
            # apitype 1 = premium 30 days
            apitype = 0 if timeto > datetime.now() - timedelta(days=7) else 1

            res = self.twitter.get_tweets(query, timefrom.strftime("%Y-%m-%d"),
                                                 timeto.strftime("%Y-%m-%d"),
                                          num, location, apitype=apitype)

            tweets = []  # list of Tweet object
            i = 0
            for tweet in res:
                # location object storing location data from the tweet json
                loc = DataStructures.Location(None, None, None, None, None, None, None)
                qcount = 0   # number of quotes
                rcount = 0   # number of replies

                # TODO: need changes to all the locations values. probably isn't accurate right now
                if tweet['geo'] is not None:
                    if ('coordinates' in tweet['geo']) and tweet['geo']['coordinates']:
                        coord = tweet['geo']['coordinates']
                        loc = self.get_location_by_latlon(float(coord[0]), float(coord[1]))

                if 'quote_count' in tweet:
                    # store tweet['quote_count'] in qcount
                    qcount = tweet['quote_count']

                if 'reply_count' in tweet:
                    # store tweet['reply_count'] in rcount
                    rcount = tweet['reply_count']

                # TODO: need changes to all the locations values. probably isn't accurate right now
                temptweet = DataStructures.Tweet(id=i,
                                                 ids=tweet['id'],
                                                 uid=tweet['user']['id'],
                                                 cont=tweet['text'],
                                                 lat=loc.latitude, lon=loc.longitude, locid=loc.woeid, # location isfound in tweet['geo']
                                                 likes=tweet['favorite_count'],
                                                 quotes=qcount,
                                                 rtweets=tweet['retweet_count'],
                                                 repl=rcount,
                                                 date=tweet['created_at'])
                tweets.append(temptweet)
                i += 1

            # SORT the tweets returned by the retweet_count
            # Sorting will ruin the true "local" trends.
            if sort == 1:
                print("SORTING TWEETS")
                AlgorithmsManager.sort_tweets(tweets)

            tweets_n = []
            for k in range(0, min(num, len(tweets))):
                tweets_n.append(tweets[k].__dict__)

            self.cache.add(querystr, tweets, cachetime)
            return tweets_n

        else:
            print("\nReturning [", querystr, "] from cache\n")
            tweets = self.cache.retrieve(querystr)
            tweets_n = []
            for k in range(0, min(num, len(tweets))):
                tweets_n.append(tweets[k].__dict__)
            return tweets_n
    # end get_top_tweets_from_query

    # return a Location object
    # pass in an address string
    # Example addrstr: "1801 N Broad St, Philadelphia, PA 19122"
    def get_location_by_address(self, address):
        # TODO: possibly access database to check for existing location
        lat, lon = geocoding(address)
        res = self.twitter.get_closest_location(lat, lon)
        return self.parse_location_json(res, lat, lon)

    # return a Location object
    # pass in latitude and longitude values
    # lat lon must be numeric strings or floats
    def get_location_by_latlon(self, lat, lon):
        # TODO: possibly access database to check for existing location
        res = self.twitter.get_closest_location(float(lat), float(lon))
        return self.parse_location_json(res, float(lat), float(lon))

    # take in a woeid and return a locations object
    def get_location_by_woeid(self, woeid):
        # TODO: possibly access the database here
        return {}

    def get_all_locations(self):
        # queryres row entry format:
        #     woe_id, city, states, lat, long
        queryres = self.database.query('SELECT * FROM locations;')
        resrows = queryres.get_rows()
        resarr = []
        for row in resrows:
            resarr.append(DataStructures.Location(row[0], row[1], row[2], None, row[0], row[3], row[4]).__dict__)
        return resarr


        return queryres

    # parse the location json returned by twitter.get_closest_location
    # args:
    #   the json object
    #   the latitude and longitude of the location as floats
    def parse_location_json(self, loc, lat, lon):
        name = loc['name']
        parentid = loc['parentid']
        country = loc['country']
        woeid = loc['woeid']
        countryCode = loc['countryCode']

        location = DataStructures.Location(0, name, None, parentid, woeid, lat, lon)
        return location

    # pass in array of Trend object and this will sort it using insertion sort
    @staticmethod
    def sort_trends(arr):
        length = len(arr)
        for l in range(1, length):
            temp = arr[l]
            tempval = temp.tweet_volume
            k = l-1
            while k >= 0 and    (tempval if tempval is not None else 0) >= \
                                (arr[k].tweet_volume if arr[k].tweet_volume is not None else 0):
                arr[k+1] = arr[k]
                k -= 1
            arr[k+1] = temp


    # pass in array of Tweet object and this will sort it using insertion sort
    @staticmethod
    def sort_tweets(arr):
        length = len(arr)
        for l in range(1, length):
            temp = arr[l]
            tempval = temp.retweets
            k = l - 1
            while k >= 0 and (tempval if tempval is not None else 0) >= \
                    (arr[k].retweets if arr[k].retweets is not None else 0):
                arr[k + 1] = arr[k]
                k -= 1
            arr[k + 1] = temp

    # function that takes two strings and return an HTML text in a format like:
    #       REQUIRED
    #       [arg1]
    #       [arg2]
    #
    #       optional
    #       [arg1]
    #       [arg2]
    @staticmethod
    def get_args_as_html_str(required, optional):
        htmlstr = ""
        if len(required) > 0:
            htmlstr += "<b>REQUIRED</b><br>"
            for arg in required:
                htmlstr += "["+arg+"]<br>"
            htmlstr += "<br>"
        if len(optional) > 0:
            htmlstr += "<i><b>optional</b></i><br>"
            for arg in optional:
                htmlstr += "["+arg+"]<br>"
        return htmlstr


