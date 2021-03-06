
# DataStructures.py contains python class representation of database tables
# Classes blueprint are referenced from Design Document II under [Database] section
# TODO: If needed, this file can be updated to add and remove attributes or classes


# [Tweet class]
class Tweet:

    def __init__(self, id, ids, uid, uname, cont, lat, lon, locid, likes, quotes, rtweets, repl, date, url):
        self.tweet_PK = id
        self.tweet_id_str = ids
        self.userid = uid
        self.username = uname
        self.content = cont
        self.latitude = lat
        self.longitude = lon
        self.location_id = locid
        self.likes = likes
        self.quotes = quotes
        self.retweets = rtweets
        self.replies = repl
        self.tweet_date = date
        self.url = url

# end Tweet class


# [User class]
class User:

    def __init__(self, id, ids, uname, name, signup, loc, protected, folcount, fricount):
        self.user_PK = id
        self.user_id = ids
        self.username = uname
        self.name = name
        self.signup_date = signup
        self.location = loc
        self.protected = protected
        self.followers_count = folcount
        self.friends_count = fricount

# end User class


# [Follower class]
class Follower:

    def __init__(self, uid1, uid2):
        self.user1_id = uid1
        self.user2_id = uid2

# end Follower class


# [Trend class]
class Trend:

    def __init__(self, id, cont, istag, query, volume, timestamp=None):
        self.trend_PK = id
        self.trend_content = cont
        self.is_hashtag = istag
        self.query_term = query
        self.tweet_volume = volume

# end Trend


# [TrendsSnapshot class]
class TrendsSnapshot:
    # trends is an array of Trend objects in dictionary format
    # loc is a Location object in dictionary format
    def __init__(self, snapid, trends, woeid, timestamp):
        self.snapid = snapid
        self.trends = trends
        self.woeid = woeid
        self.timestamp = timestamp

    # create a trendsnapshot object
    @staticmethod
    def create_trends_snapshot(snapid, trends, loc, timestamp):
        snap = TrendsSnapshot(snapid, trends, int(loc['woeid']), timestamp)
        return snap

# [TrendTweetsSnapshot class]
class TrendTweetsSnapshot:

    def __init__(self, id, trpk, twpk, locpk, date):
        self.trend_tweets_snapshot_PK = id
        self.trend_PK = trpk
        self.tweet_PK = twpk
        self.location_PK = locpk
        self.timestamp = date

# end TrendTweetsSnapshot


# [Location class]
class Location:
    def __init__(self, id, ctid, stid, cnid, woeid, lat, lon):
        self.location_PK = id
        self.city_id = ctid
        self.state_id = stid
        self.country_id = cnid
        self.woeid = woeid
        self.latitude = lat
        self.longitude = lon

# end Location


# [City class]
class City:
    def __init__(self, id, name):
        self.city_PK = id
        self.city_name = name

# end City


# [State class]
class State:
    def __init__(self, id, name):
        self.state_PK = id
        self.state_name = name

# end State


# [Country class]
class Country:
    def __init__(self, id, name):
        self.country_PK = id
        self.country_name = name

# end Country
