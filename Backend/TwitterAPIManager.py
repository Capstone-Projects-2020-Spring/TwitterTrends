
# Contain the TwitterAPI Wrapper import
from wrappers.premiumAPI import premiumAPI
from wrappers.standardAPI import standardAPI
from wrappers.geocode import geocoding
import json

# Contain TwitterAPI wrapper Functions


class TwitterAPIManager:


    def __init__(self):
        self.standardAPI = standardAPI()
        self.premiumAPI = premiumAPI()


    def top_trends(self, woeid, num):
        top_trends = self.standardAPI.retrieve_trends(woeid, num)
        return top_trends


    def trends_close(self, lat, long, num):
        nearbyLocations = self.standardAPI.getTrendsClose(lat, long, num)
        return nearbyLocations


    def num_tweets(self, trend):
        ()


    def top_tweets(self, trend, num):
        top_tweets = self.premiumAPI.getTweets(trend, num)
        return top_tweets

    def sample_tweet(self, trend):
        sample_tweet = self.premiumAPI.getSampleTweet(trend)
        return sample_tweet


def geocode(address):
    ()
    return woeid        


if __name__=='__main__':
    print("\nHello from TwitterAPIManager!!\n")
    twitter = TwitterAPIManager()
    print("Twitter wrapper is created\n")

    # Test: Retrieve top trends
    woeid = 2379574
    result = twitter.top_trends(woeid, 5)
    print('Top 5 Trends in ' + result['location'])
    for i in result['trends']:
        print(i)
    
    print('\n')

    # Test: Get tweets
    trend = result['trends'][0]
    print('Tweets for ' + trend + "\n-------------")
    tweets = twitter.top_tweets(trend, 5)
    for i in tweets:
        print(i + "\n-------------")

    print('\n')

    # Test: Sample tweet
    sampleTweet = twitter.sample_tweet("coronavirus")
    print("Sample Tweet:")
    print(json.dumps(sampleTweet, indent=5))

    print('\n')

    # Test: Get WOEID from an address input by user and top trends
    address = "1800 Liacouras Walk, Philadelphia, PA 19122"
    lat, long = geocoding(address)
    print("Latitude: " + str(lat) + ", longitude: " + str(long))
    trendsClose = twitter.trends_close(lat, long, 5)
    print("Trends in Nearby Locations:")
    
    for place in trendsClose:
        print(place["name"] + ":", end= " ")
        output = twitter.top_trends(place['woeid'], 5)
        print(output['trends'])

    print('\n')