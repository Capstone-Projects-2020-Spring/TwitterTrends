import os

import searchtweets as st
import wrappers.credentials as creds

TWITTER_PREMIUM_API_ENDPOINT_FORMAT = "https://api.twitter.com/{}/tweets/search/{}/{}.json"
TWITTER_API_VERSION = "1.1"
MONTH_SEARCH_PRODUCT = "30day"
FULL_ARCHIVE_SEARCH_PRODUCT = "fullarchive"
MONTH_SEARCH_DEV_ENV_LABEL = "SSBase30DayEnv"
FULL_ARCHIVE_SEARCH_DEV_ENV_LABEL = "SSBaseFullArchiveEnv"

PREMIUM_30_DAY_ENDPOINT = TWITTER_PREMIUM_API_ENDPOINT_FORMAT.format(TWITTER_API_VERSION, MONTH_SEARCH_PRODUCT,
                                                                     MONTH_SEARCH_DEV_ENV_LABEL)
PREMIUM_FULL_ARCHIVE_ENDPOINT = TWITTER_PREMIUM_API_ENDPOINT_FORMAT.format(TWITTER_API_VERSION,
                                                                           FULL_ARCHIVE_SEARCH_PRODUCT,
                                                                           FULL_ARCHIVE_SEARCH_DEV_ENV_LABEL)

class premiumAPI:

    def __init__(self):
        self.monthSearchArgs = creds.getPremiumEndpointCreds(PREMIUM_30_DAY_ENDPOINT)
        self.st = st
        self.pytwit = creds.getPremiumPythonTwitterCreds()

    # Retrieve tweets using the Twitter premium API endpoint
    # Args:
    #   keyword: query string
    #   time: the date time of where to start searching tweets
    #   num: number of tweets to return
    def getTweets(self, keyword, timefrom, timeto, num, location=None):

        # TODO: add search tweets by location and keyword using bear/python-twitter
        if location is not None:
            radius = "100mi"
            geocode = "{},{},{}".format(location.min_latitude, location.min_longitude, radius)
            print(geocode)
            tweets = self.pytwit.GetSearch(term=keyword,
                                           geocode=geocode,
                                           since=timefrom, until=timeto,
                                           result_type='top', count=num)
            return tweets
        else:
            #rule = self.st.gen_rule_payload(keyword, from_date=st.convert_utc_time(timefrom),
            #                                to_date=st.convert_utc_time(timeto))
            #tweets = self.st.collect_results(rule, max_results=num, result_stream_args=self.monthSearchArgs)

            # retrieving tweets using python-twitter instead
            tweets = self.pytwit.GetSearch(term=keyword, since=timefrom, until=timeto,
                                           result_type='mixed', count=10)

            return tweets

    def getSampleTweet(self, keyword):
        rule = st.gen_rule_payload(keyword)
        result = self.st.collect_results(rule, max_results=1, result_stream_args= self.monthSearchArgs)
        tweet = result[0]

        tweet_info = {'content': tweet.text, 'timestamp': tweet.created_at_string,
                    'favorite count': tweet.favorite_count, 'retweet count': tweet.retweet_count,
                    'user': tweet.name, 'profile location': tweet.profile_location, 
                    'follower count': tweet.follower_count, 'geo coordinates (long/lat)': tweet.geo_coordinates}
        return tweet_info




