
# In charge of all algorithms needed by the backend server


class AlgorithmsManager:

    def __init__(self, cache, db, twit):
        self.cache = cache
        self.database = db
        self.twitter = twit

    @staticmethod
    def get_top_5_tweets_from_zip_code(zipcode):
        # translate zipcode to geolocation argument
        # use the argument to pull tweets from Twitter API
            # pull from cache or database if data already cached recently
        # sort the list of tweets based on likes and retweets
        # return the top 5
        return None

    @staticmethod
    def get_top_5_trends_from_zip_code(zipcode):
        # translate zipcode to geolocation argument
        # use the argument to pull trends from twitter API
            # pull from cache or database if data already cached recently
        # sort the list of trends based on frequency
        # return the top 5
        return None

    @staticmethod
    def get_tweets_with_keywords(tweet_sample=None, *keywords):
        # maybe reference Aho–Corasick algorithm
        # if tweet_sample is None
            # use Cache/Database/Twitter API to retrieve a set of tweets
            # Filter the tweets to only retain the ones with keywords
        # else
            # Filter the tweets from tweet_sample to only retain the ones with keywords
        # return filtered list of tweets
        return None