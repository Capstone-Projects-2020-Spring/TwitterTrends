import wrappers.credentials as creds

class standardAPI:

    def __init__(self):
        self.tweepy = creds.getStandardTweepyTwitterCreds()

    def retrieve_trends(self, woeid):
        trends = self.tweepy.trends_place(woeid)
        # top_trends  = self.query_transform(query, woeid, num)
        return trends

    def get_nearby_location(self, lat, long):
        location = self.tweepy.trends_closest(lat, long)
        return location

    # Retrieve tweets using the Twitter 7 Days STANDARD API endpoint
    # Args:
    #   keyword: query string
    #   since: the date string of where to start searching tweets
    #   until : end date string of where to stop searching tweets
    #   num: number of tweets to return
    #   location: optional location object
    def getTweets(self, keyword, since, until, num, location=None):

        if location is not None:
            radius = "100mi"
            geocode = "{},{},{}".format(location.latitude, location.longitude, radius)

            # # # old version with python-twitter
            #tweets = self.pytwit.GetSearch(term=keyword,
            #                               geocode=geocode,
            #                               since=since, until=until,
            #                               result_type='top', count=num)

            tweets = self.tweepy.search(q=keyword, geocode=geocode, since=since, until=until, result_type='top', count=num)

            # # # Parsing tweepy output to our standardized format
            #  tweepy returns array of Status objects
            tweetsparsed = []
            for status in tweets:
                tweetsparsed.append(status._json)

            return tweetsparsed
        else:
            tweets = self.tweepy.search(q=keyword, since=since, until=until,
                                           result_type='top', count=num)

            # # # Parsing tweepy output to our standardized format
            #  tweepy returns array of Status objects
            tweetsparsed = []
            for status in tweets:
                tweetsparsed.append(status._json)

            return tweetsparsed

    def getUsernameFromID(self, id2):
        user = self.tweepy.get_user(id2)
        return user._json['screen_name']

    # get list of recent tweets from a user
    def getTweetsFromUser(self, id2, username, count=20):
        # get tweets from user ID
        queryusertweets = []
        try:
            if username is not None:
                queryusertweets = self.tweepy.user_timeline(screen_name=username, count=count)
            elif id2 > 0:
                queryusertweets = self.tweepy.user_timeline(id=id2, count=count, page=0)
            else:
                return queryusertweets
        except:
            print("Can't access user timeline")

        texts = []
        for status in queryusertweets:
            texts.append(status._json['text'])
        return texts

    # get list of userID in a user's follow list
    def getFollowersID(self, id2, username, count=20):
        queryfriends_ids = []
        if username is not None:
            queryfriends_ids = self.tweepy.friends_ids(screen_name=username)
        elif id2 > 0:
            queryfriends_ids = self.tweepy.friends_ids(id=id2)
        else:
            return queryfriends_ids

        trimmedids = []
        # only check up to first 3 of the followers id
        # initial implementation to speed up word cloud generation time
        for i in range(0, min(3, len(queryfriends_ids))):
            trimmedids.append(queryfriends_ids[i])
        return trimmedids

    def query_transform(self, json_result, woeid, num):
        trendsResult = json_result[0]
        place = trendsResult['locations'][0]['name']
        trends_list = trendsResult['trends']
        trends = []
        for i in range(0, num):
            trends.append(trends_list[i]['name'])
        timestamp = trendsResult['as_of']

        trends_dict = {'location': place, 'woeid': woeid, 'trends': trends, 'time': timestamp}
        return trends_dict