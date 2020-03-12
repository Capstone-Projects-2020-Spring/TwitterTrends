
# Contain the TwitterAPI Wrapper import
from wrappers.premiumAPI import premiumAPI
from wrappers.standardAPI import standardAPI
from wrappers.geocode import geocoding
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
    #   timefrom: starting date time of the search
    #   timeto: ending date time of the search
    #   num: optional value. max amount of tweets returned. default to 10
    #   location: optional and is set to none by default.
    #               Location will greatly decrease returned tweets volume
    def get_tweets(self, trend, timefrom, timeto, num=10, location=None):
        # num arg maybe not needed?
        top_tweets = self.premiumAPI.getTweets(trend, timefrom, timeto, num, location)
        return top_tweets

    # sample tweet function that returns a tweet based on a given search query
    def sample_tweet(self, trend):
        sample_tweet = self.premiumAPI.getSampleTweet(trend)
        return sample_tweet


def geocode(address):
    ()
    return woeid        


# # # # # # # # # # # # # # # # #
# BELOW ARE TEST CODE FOR TwitterAPI

if __name__=='__main__':
    print("\nHello from TwitterAPIManager!!\n")
    twitter = TwitterAPIManager()
    print("Twitter wrapper is created\n")

    # Test: Retrieve top trends
    woeid = 2379574
    result = twitter.top_trends(woeid)
    print(result)
    #print('Top 5 Trends in ' + result['location'])
    #for i in result['trends']:
    #    print(i)
    
    print('\n')

    # Test: Get tweets
    #trend = result['trends'][0]
    trend = "#temple"
    print('Tweets for ' + trend + "\n-------------")
    ##tweets = twitter.top_tweets(trend, "2020-02-20", "2020-02-25", 1)
    #print(tweets)
    #for i in tweets:
    #    print(i)

    #print('\n')


    ### commented out because broken
    # Test: Sample tweet
    #sampleTweet = twitter.sample_tweet("coronavirus")
    print("Sample Tweet:")
    #print(json.dumps(sampleTweet, indent=5))

    print('\n')

    # Test: Get WOEID from an address input by user and top trends
    address = "1801 N Broad St, Philadelphia, PA 19122"  # Temple's address
    lat, long = geocoding(address)
    print("Latitude: " + str(lat) + ", longitude: " + str(long))
    trendsClose = twitter.get_closest_location(lat, long)
    print("Trends in Nearby Locations:")

    print(trendsClose)

    #for place in trendsClose:
    #    print(place["name"] + ":", end= " ")
    #    output = twitter.top_trends(place['woeid'], 5)
    #    print(output['trends'])


    print('\n')
