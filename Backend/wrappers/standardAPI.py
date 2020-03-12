import wrappers.credentials as creds

class standardAPI:

    def __init__(self):
        self.tweepy = creds.getStandardTweepyTwitterCreds()
        self.pytwit = creds.getStandardPythonTwitterCreds()

    def retrieve_trends(self, woeid):
        query = self.tweepy.trends_place(woeid)
        # top_trends  = self.query_transform(query, woeid, num)
        return query

    def get_nearby_location(self, lat, long):
        query = self.tweepy.trends_closest(lat, long)
        return query

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
            geocode = "{},{},{}".format(location.min_latitude, location.min_longitude, radius)
            print(geocode)
            tweets = self.pytwit.GetSearch(term=keyword,
                                           geocode=geocode,
                                           since=since, until=until,
                                           result_type='top', count=num)

            return tweets
        else:
            tweets = self.pytwit.GetSearch(term=keyword, since=since, until=until,
                                           result_type='top', count=num)

            return tweets

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