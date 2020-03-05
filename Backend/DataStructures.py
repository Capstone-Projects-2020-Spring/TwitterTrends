
# DataStructures.py contains python class representation of database tables
# Classes blueprint are referenced from Design Document II under [Database] section
# TODO: If needed, this file can be updated to add and remove attributes or classes


# [Tweet class]
class Tweet:

    def __init__(self, uid, userid, cont, loc, likes, rtweet, clicks, views, date):
        self.tweet_id = uid
        self.user_id = userid
        self.content = cont
        self.location = loc
        self.likes = likes
        self.retweets = rtweet
        self.clicks = clicks
        self.views = views
        self.tweet_date = date

# end Tweet class


# [User class]
class User:

    def __init__(self, uid, uname, signdate):
        self.user_id = uid
        self.user_name = uname
        self.signup_date = signdate

# end User class


# [Followers class]
class Followers:

    def __init__(self, uid1, uid2, folDate):
        self.user1_id = uid1
        self.user2_id = uid2
        self.follow_date = folDate

# end Followers class


# [TweetsWithTags class]
class TweetsWithTag:

    def __init__(self, tagid, tweetid, tagname):
        self.hashtag_id = tagid
        self.tweet_id = tweetid
        self.hashtag_name = tagname

# end class TweetsWithTag


# [Hashtag class]
class Hashtag:

    def _init_(self, tagid, tagname, freq):
        self.hashtag_id = tagid
        self.hashtag_name = tagname
        self.frequency = freq

# end class Hashtag


# [LocationMap class]
class LocationMap:

    def __init__(self, locid, city, state):
        self.location_id = locid
        self.city = city
        self.state = state

# end class LocationMap


# [TweetsByLocation class]
class TweetsByLocation:

    def __init__(self, loc, tweetid):
        self.location = loc
        self.tweet_id = tweetid

# end class TweetsByLocation


# [TrendsByLocation class]
class TrendsByLocation:

    def __init__(self, loc, tagname):
        self.location = loc
        self.tag_name = tagname

# end class TrendsByLocation
