from tweepy import RateLimitError

import wrappers.credentials as creds
import tweepy as tw

class standardAPI:

    def __init__(self):
        self.tweepy = creds.getStandardTweepyTwitterCreds(0)
        # interfaces to the twitter API using different developer account credentials (to get around rate limits)
        backupTweepy1 = creds.getStandardTweepyTwitterCreds(1)
        backupTweepy2 = creds.getStandardTweepyTwitterCreds(2)
        self.backupTweepysQueue = [backupTweepy1, backupTweepy2]
        self.tweepyAccountIndex = 0

    def _rotate_tweepy_accounts(self):
        exhaustedTweepy = self.tweepy
        freshTweepy = self.backupTweepysQueue.pop(0)
        self.tweepy = freshTweepy
        self.backupTweepysQueue.append(exhaustedTweepy)
        numTweepyAccounts = len(self.backupTweepysQueue) + 1
        self.tweepyAccountIndex = (self.tweepyAccountIndex + 1) % numTweepyAccounts
        print("previous twitter account hit rate limit, switching to account #", self.tweepyAccountIndex)

    def retrieve_trends(self, woeid):
        try:
            trends = self.tweepy.trends_place(woeid)
        except RateLimitError as rle:
            print("hit rate limit while retrieving trends for a woeid ", woeid)
            self._rotate_tweepy_accounts()
            trends = self.tweepy.trends_place(woeid)

        # top_trends  = self.query_transform(query, woeid, num)
        return trends

    def get_nearby_location(self, lat, long):
        try:
            location = self.tweepy.trends_closest(lat, long)
        except RateLimitError as rle:
            print("hit rate limit while finding a location near lat-long coordinates ", lat, ", ", long)
            self._rotate_tweepy_accounts()
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
            try:
                tweets = self.tweepy.search(q=keyword, geocode=geocode, since=since, until=until, result_type='top',
                                            count=num)
            except RateLimitError as rle:
                self._rotate_tweepy_accounts()
                print("hit rate limit while fetching tweets about ", keyword, " within a region")
                tweets = self.tweepy.search(q=keyword, geocode=geocode, since=since, until=until, result_type='top',
                                            count=num)

            # # # Parsing tweepy output to our standardized format
            #  tweepy returns array of Status objects
            tweetsparsed = []
            for status in tweets:
                tweetsparsed.append(status._json)

            return tweetsparsed
        else:
            try:
                tweets = self.tweepy.search(q=keyword, since=since, until=until, result_type='top', count=num)
            except RateLimitError as rle:
                self._rotate_tweepy_accounts()
                print("hit rate limit while fetching tweets about ", keyword)
                tweets = self.tweepy.search(q=keyword, since=since, until=until, result_type='top', count=num)

            # # # Parsing tweepy output to our standardized format
            #  tweepy returns array of Status objects
            tweetsparsed = []
            for status in tweets:
                tweetsparsed.append(status._json)

            return tweetsparsed

    def getUsernameFromID(self, id2):
        try:
            user = self.tweepy.get_user(id2)
        except RateLimitError as rle:
            self._rotate_tweepy_accounts()
            print("hit rate limit while fetching the screen name of a user based on their user id ", id2)
            user = self.tweepy.get_user(id2)

        return user._json['screen_name']

    # get list of recent tweets from a user
    def getTweetsFromUser(self, id2, username, count=20):
        # get tweets from user ID
        queryusertweets = []
        try:
            if username is not None:
                try:
                    queryusertweets = self.tweepy.user_timeline(screen_name=username, count=count)
                except RateLimitError as rle:
                    self._rotate_tweepy_accounts()
                    print("hit rate limit while fetching a user's recent tweets based on their screen name ", username)
                    queryusertweets = self.tweepy.user_timeline(screen_name=username, count=count)
            elif id2 > 0:
                try:
                    queryusertweets = self.tweepy.user_timeline(id=id2, count=count, page=0)
                except RateLimitError as rle:
                    self._rotate_tweepy_accounts()
                    print("hit rate limit while fetching a user's recent tweets based on their user id ", id2)
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
    def getFriendsID(self, id2, username, count=3):
        queryfriends_ids = []
        if username is not None:
            try:
                queryfriends_ids = self.tweepy.friends_ids(screen_name=username)
            except RateLimitError as rle:
                self._rotate_tweepy_accounts()
                print("hit rate limit while fetching the friends of a user ", username)
                queryfriends_ids = self.tweepy.friends_ids(screen_name=username)
        elif id2 > 0:
            try:
                queryfriends_ids = self.tweepy.friends_ids(id=id2)
            except RateLimitError as rle:
                self._rotate_tweepy_accounts()
                queryfriends_ids = self.tweepy.friends_ids(id=id2)
        else:
            return queryfriends_ids

        #todo remove or lessen this restriction?
        trimmedids = []
        # only include to first 3 of the friends' ids
        # initial implementation to speed up word cloud generation time
        for i in range(0, min(count, len(queryfriends_ids))):
            trimmedids.append(queryfriends_ids[i])
        return trimmedids

    # get list of userID in a user's follower list
    def getFollowersID(self, id2, username, count=3):
        queryFollowers_ids = []
        if username is not None:
            try:
                queryFollowers_ids = self.tweepy.followers_ids(screen_name=username)
            except RateLimitError as rle:
                self._rotate_tweepy_accounts()
                print("hit rate limit while fetching the followers of a user ", username)
                queryFollowers_ids = self.tweepy.followers_ids(screen_name=username)
        elif id2 > 0:
            try:
                queryFollowers_ids = self.tweepy.followers_ids(id=id2)
            except RateLimitError as rle:
                self._rotate_tweepy_accounts()
                queryFollowers_ids = self.tweepy.followers_ids(id=id2)
        else:
            return queryFollowers_ids

        # todo remove or lessen this restriction?
        trimmedids = []
        # only check up to first 3 of the followers' ids
        # initial implementation to speed up word cloud generation time
        for i in range(0, min(count, len(queryFollowers_ids))):
            trimmedids.append(queryFollowers_ids[i])
        return trimmedids

    # Get twitter user profile with screen_name (e.g. @ttclaire2)
    #   return type: a twitter User object
    def get_user(self, public_id):
        try:
            user_object = self.tweepy.get_user(id=None, user_id=None, screen_name=public_id)
        except RateLimitError as rle:
            self._rotate_tweepy_accounts()
            print("hit rate limit while getting a detailed description of a user ", public_id)
            user_object = self.tweepy.get_user(id=None, user_id=None, screen_name=public_id)

        return user_object

    # Get the followers of the specified user 
    #   return type: a list of twitter User objects
    # TODO: handling exception Tweepy.Error
    def get_followers(self, public_id, max_num):
        followerList = []
        try:
            for follower in tw.Cursor(self.tweepy.followers, screen_name=public_id).items(max_num):
                followerList.append(follower)
        except RateLimitError as rle:
            self._rotate_tweepy_accounts()
            print("hit rate limit while fetching the followers of a user ", public_id)
            #resetting it because you can't know
            # how far the previous attempt got before hitting the rate limit
            followerList = []
            for follower in tw.Cursor(self.tweepy.followers, screen_name=public_id).items(max_num):
                followerList.append(follower)


        return followerList

    # Get the most recent tweets of the specified user
    #   return: count passed as parameter, or the total number of available tweets
    def get_user_timeline(self, public_id, max_num=30):
        timeline = []
        try:
            for status in tw.Cursor(self.tweepy.user_timeline, screen_name=public_id).items(max_num):
                timeline.append(status)
        except RateLimitError as rle:
            self._rotate_tweepy_accounts()
            print("hit rate limit while fetching the full contents of the timeline of a user ", public_id)
            # resetting it because you can't know
            # how far the previous attempt got before hitting the rate limit
            timeline = []
            for status in tw.Cursor(self.tweepy.user_timeline, screen_name=public_id).items(max_num):
                timeline.append(status)

        return timeline

    # Get a list of random retweets for a given tweet ID
    #   args: tweet ID, count (max = 100)
    #   return type: a list of Twitter status objects 
    # Sometimes the number returned is less than input

    # TODO: handling exception Tweepy.Error
    
    def get_retweets_of_tweet(self, tweet_id, max_num=100):
        retweets = []
        try:
            retweets = self.tweepy.retweets(id=tweet_id, count=max_num)
        except RateLimitError as rle:
            self._rotate_tweepy_accounts()
            print("hit rate limit while loading the id's of the retweets of a tweet which had id ", tweet_id)
            retweets = self.tweepy.retweets(id=tweet_id, count=max_num)

        return retweets

    # Get a list of random retweeters for a given tweet ID
    #   return type: a list of Twitter user objects
    def get_retweeters_of_tweet(self, tweet_id, max_num=100):
        retweeters = []
        retweets = self.get_retweets_of_tweet(tweet_id, max_num)
        for tweet in retweets:
            user = tweet.user #User object
            retweeters.append(user)
        return retweeters

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

if __name__ == "__main__":

    api = standardAPI()

    timeline = api.get_user_timeline('realDonaldTrump', max_num=1)
    status = timeline[0]
    count = 0

    tweetID = status.id
    print("Tweet ID: ", tweetID)
    retweeters = api.get_retweeters_of_tweet(tweetID, max_num=30)
    for each in retweeters:
        count += 1
        # print(each, "\n")

    print("Count: ", count)


