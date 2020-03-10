from datetime import datetime, timedelta


from flask import jsonify
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
    def get_top_num_trends_from_location(self, woeid, num, querystr):

        cachetime = 2  # 2 minutes cache time check

        if self.cache.should_update(querystr, cachetime):

            query = self.twitter.top_trends(woeid)  # api.trends_place(woeid)

            # Variables storing other info about the trends
            as_of = query['as_of']
            created_at = query['created_at']
            loc_name = query['locations'][0]['name']
            loc_woeid = query['locations'][0]['woeid']

            trends = []
            i = 0
            for trend in query['trends']:
                vol = trend['tweet_volume']
                tempTrend = DataStructures.Trend(0,
                                                 trend['name'],
                                                 True if trend['name'][0] == '#' else False,
                                                 trend['query'],
                                                 vol)

                trends.append(tempTrend)
                i += 1

            # SORT the trends returned by the tweet volume
            # Sorting will ruin the true "local" trends.
            #       it will sort by OVERALL tweet volume of any trends
            # UNCOMMENT to sort
            # AlgorithmsManager.insertion_sort_trends(trends)

            trends_n = []

            for k in range(0, min(num, len(trends))):
                trends_n.append(trends[k].__dict__)

            json = jsonify(trends_n)
            self.cache.add(querystr, json, 2)
            return jsonify(trends_n)
        else:
            print("\nReturning", querystr , "from cache\n")
            return self.cache.retrieve(querystr)


    def get_tweets_with_keywords(self, tweet_sample=None, *keywords):
        # maybe reference Aho–Corasick algorithm
        # if tweet_sample is None
            # use Cache/Database/Twitter API to retrieve a set of tweets
            # Filter the tweets to only retain the ones with keywords
        # else
            # Filter the tweets from tweet_sample to only retain the ones with keywords
        # return filtered list of tweets
        tweets = ["tweet 1 keyword 1 1", "tweet 2 keyword 2 2", "tweet 3 keyword 3 3",
                  "tweet 4 keyword 4 4", "tweet 5 keyword 5 5", "tweet 6 keyword 6 6",
                  "tweet 7 keyword 7 7", "tweet 8 keyword 8 8", "tweet 9 keyword 9 9"]
        return tweets

    # pass in array of Trend object and this will sort it using insertion sort
    @staticmethod
    def insertion_sort_trends(trends):
        length = len(trends)
        for l in range(1, length):
            temp = trends[l]
            tempvol = temp.tweet_volume
            k = l-1
            while k >= 0 and    (tempvol if tempvol is not None else 0) >= \
                                (trends[k].tweet_volume if trends[k].tweet_volume is not None else 0):
                trends[k+1] = trends[k]
                k -= 1
            trends[k+1] = temp


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