
from TwitterAPIManager import TwitterAPIManager
from flask import jsonify
import DataStructures

# In charge of all algorithms needed by the backend server


class AlgorithmsManager:

    def __init__(self, cache, db, twit):
        self.cache = cache
        self.database = db
        self.twitter = twit

    def get_top_5_tweets_from_location(self, woeid, num):
        # use the woeid argument to pull tweets from Twitter API
            # pull from cache or database if data already cached recently
        # sort the list of tweets based on tweet volume
        # return the top 5 as json

        # api.verify_credentials()
        # print("Valid credentials")

        woeid = woeid
        query =  self.twitter.top_trends(woeid) #api.trends_place(woeid)
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
            if l + 1 < length:
                temp = trends[l + 1]
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


        tweets = ["tweet 1 hahahahhaha", "tweet 2 dasdoadkoafkw", "tweet 3  d123@!321321wd",
                  "tweet 4 dad2182138123123123", "tweet 5 d21332132!##!!#@@!#@!#"]
        return tweets

    def get_top_5_trends_from_location(self, woeid):
        # use the woeid argument to pull tweets from Twitter API
            # pull from cache or database if data already cached recently
        # sort the list of tweets based on tweet volume
        # return the top 5 as json
        tweets = ["#trends1", "#trends2", "#trends3", "#trends4", "#trends5"]
        return tweets

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
