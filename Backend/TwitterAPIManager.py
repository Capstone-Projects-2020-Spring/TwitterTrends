
# Contain the TwitterAPI Wrapper import
from wrappers.premiumAPI import premiumAPI
from wrappers.standardAPI import standardAPI
from wrappers.geocode import geocoding

from datetime import datetime, timedelta
import json

# Contain TwitterAPI wrapper Functions

# TERRA woeid : 23424775

class TwitterAPIManager:

    def __init__(self):
        self.standardAPI = standardAPI()
        self.premiumAPI = premiumAPI()

    # Arguments are
    #   location woeid
    #   top num trends
    def top_trends(self, woeid):
        top_trends = self.standardAPI.retrieve_trends(woeid)
        return top_trends[0]

    # Arguments are
    #   location latitude and longitude
    #   return a json containing the closest location to specified lat lon
    def get_closest_location(self, lat, long):
        nearbyLocations = self.standardAPI.get_nearby_location(lat, long)
        return nearbyLocations[0]

    def num_tweets(self, trend):
        ()

    # get an array of tweets jsons given a trend, datetime, and amount returned
    # args:
    #   trend: query search terms
    #   timefrom: date string. From when to search. YYYY-MM-DD
    #   timeto: date string. To when the search end. YYYY-MM-DD
    #   num: optional value. max amount of tweets returned. default to 10
    #   location: optional and is set to none by default.
    #               Location will greatly decrease returned tweets volume
    def get_tweets(self, trend, timefrom, timeto, num=10, location=None, apitype=0):
        # num arg maybe not needed?
        if apitype == 0:
            print("USING STANDARD TWEET")
            return self.standardAPI.getTweets(trend, timefrom, timeto, num, location)
        else:
            print("USING PREMIUM TWEET")
            return self.premiumAPI.getTweets(trend, timefrom, timeto, num, location)

    # sample tweet function that returns a tweet based on a given search query
    def sample_tweet(self, trend):
        sample_tweet = self.premiumAPI.getSampleTweet(trend)
        return sample_tweet
