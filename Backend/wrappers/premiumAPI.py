import os

import searchtweets as st
import wrappers.credentials as creds

TWITTER_PREMIUM_API_ENDPOINT_FORMAT = "https://api.twitter.com/{}/tweets/search/{}/{}.json"
TWITTER_PREMIUM_API_ENDPOINT_SHORT_FORMAT = "tweets/search/{}"
TWITTER_API_VERSION = "1.1"
MONTH_SEARCH_PRODUCT = "30day"
FULL_ARCHIVE_SEARCH_PRODUCT = "fullarchive"
MONTH_SEARCH_DEV_ENV_LABEL = "premium" # "SSBase30DayEnv"
FULL_ARCHIVE_SEARCH_DEV_ENV_LABEL = "SSBaseFullArchiveEnv"

PREMIUM_30_DAY_ENDPOINT = TWITTER_PREMIUM_API_ENDPOINT_FORMAT.format(TWITTER_API_VERSION, MONTH_SEARCH_PRODUCT,
                                                                     MONTH_SEARCH_DEV_ENV_LABEL)
PREMIUM_30_DAY_ENDPOINT_SHORT = TWITTER_PREMIUM_API_ENDPOINT_SHORT_FORMAT.format(MONTH_SEARCH_PRODUCT)
PREMIUM_FULL_ARCHIVE_ENDPOINT = TWITTER_PREMIUM_API_ENDPOINT_FORMAT.format(TWITTER_API_VERSION,
                                                                           FULL_ARCHIVE_SEARCH_PRODUCT,
                                                                           FULL_ARCHIVE_SEARCH_DEV_ENV_LABEL)

class premiumAPI:

    def __init__(self):
        self.monthSearchArgs = creds.getPremiumEndpointCreds(PREMIUM_30_DAY_ENDPOINT)
        self.st = st


    # Retrieve tweets using the Twitter premium API endpoint
    # Args:
    #   keyword: query string
    #   since: the date string of where to start searching tweets
    #   until : end date string of where to stop searching tweets
    #   num: number of tweets to return
    #   location: optional location object
    def getTweets(self, keyword, timefrom, timeto, num, location=None):

            # implementation with searchtweets
            rule = self.st.gen_rule_payload(keyword, from_date=st.convert_utc_time(timefrom),
                                            to_date=st.convert_utc_time(timeto))

            tweets = self.st.collect_results(rule, max_results=num, result_stream_args=self.monthSearchArgs)
            return tweets

            ##r = self.twitapi.request('tweets/search/premium/', {'query': keyword})

            ##return r

    def getSampleTweet(self, keyword):
        rule = st.gen_rule_payload(keyword)
        result = self.st.collect_results(rule, max_results=1, result_stream_args= self.monthSearchArgs)
        tweet = result[0]

        tweet_info = {'content': tweet.text, 'timestamp': tweet.created_at_string,
                    'favorite count': tweet.favorite_count, 'retweet count': tweet.retweet_count,
                    'user': tweet.name, 'profile location': tweet.profile_location, 
                    'follower count': tweet.follower_count, 'geo coordinates (long/lat)': tweet.geo_coordinates}
        return tweet_info




