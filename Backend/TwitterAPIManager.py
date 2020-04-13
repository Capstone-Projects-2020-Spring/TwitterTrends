
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

    def getTweetsFromUser(self, id2, username, count):
        return self.standardAPI.getTweetsFromUser(id2, username)

    def getFriendsID(self, id2, username, count):
        return self.standardAPI.getFriendsID(id2, username)

    def get_username_from_id(self, id2):
        return self.standardAPI.getUsernameFromID(id2)

    # sample tweet function that returns a tweet based on a given search query
    def sample_tweet(self, trend):
        sample_tweet = self.premiumAPI.getSampleTweet(trend)
        return sample_tweet

    # get a Twitter user object
    def get_user(self, username):
        user = self.standardAPI.get_user(username)
        return user

    # get the follower network
    #   return: a list of Twitter user objects
    def followers(self, username, count):
        network = self.standardAPI.get_followers(username, count)
        return network

    # retrieves a list of retweeters by going through the most recent tweets by user
    #   args:   num_tweets (optional/default): the number of tweets to search
    #   return: a list of dictionary
    def most_recent_retweeters(self, username, num_tweets=20, num_retweets=100):
        retweetData = []
        recentTweets = self.standardAPI.get_user_timeline(username, num_tweets)

        for tweet in recentTweets:
            tweet_id = tweet.id 
            # print("Tweet ID: ", tweet_id)

            # get up to 100 random retweeters of each status
            retweeterList = self.standardAPI.get_retweeters_of_tweet(tweet_id, num_retweets)
            usernames = []
            for retweeter in retweeterList:
                usernames.append(retweeter.screen_name)

            # define the dictionary
            status = {}
            status['tweet_id'] = tweet_id
            status['retweeters_count'] = len(usernames)
            status['retweeters'] = usernames 

            retweetData.append(status)

        return retweetData