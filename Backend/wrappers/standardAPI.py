import tweepy

import wrappers.credentials as creds


class standardAPI:

    def __init__(self):
        self.api = creds.create()


    def retrieve_trends(self, woeid, num):
        query = self.api.trends_place(woeid)
        top_trends  = self.query_transform(query, woeid, num)
        return top_trends


    def getTrendsClose(self, lat, long, num):
        query = self.api.trends_closest(lat, long)
        return query
    

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