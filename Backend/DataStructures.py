
# DataStructures.py contains python class representation of database tables
# Classes blueprint are referenced from Design Document II under [Database] section
# TODO: If needed, this file can be updated to add and remove attributes or classes


# [Tweet class]
class Tweet:

    def __init__(self, id, ids, uid, cont, lat, lon, locid, likes, quotes, rtweets, repl, date):
        self.tweet_PK = id
        self.tweet_id_str = ids
        self.content = cont
        self.latitude = lat
        self.longitude = lon
        self.location_id = locid
        self.likes = likes
        self.quotes = quotes
        self.retweets = rtweets
        self.replies = repl
        self.tweet_date = date

# end Tweet class


# [User class]
class User:

    def __init__(self, id, ids, uname, signup, loc, protected, folcount, fricount):
        self.user_PK = id
        self.user_id = ids
        self.username = uname
        self.signup_date = signup
        self.location_id = loc
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

    def __init__(self, id, cont, istag):
        self.trend_PK = id
        self.trend_content = cont
        self.is_hashtag = istag

# end Trend


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
    def __init__(self, id, ctid, stid, cnid, woeid, minlat, maxlat, minlon, maxlon):
        self.location_PK = id
        self.city_id = ctid
        self.state_id = stid
        self.country_id = cnid
        self.woeid = woeid
        self.min_latitude = minlat
        self.max_latitude = maxlat
        self.min_longitude = minlon
        self.max_longitude = maxlon

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


# [TrendSnapshot class]
class TrendSnapshot:
    def __init__(self, id, time, locfk, trendfk, rank, tvol24h):
        self.trend_snapshot_PK = id
        self.timestamp = time
        self.location_PK = locfk
        self.trend_FK = trendfk
        self.rank = rank
        self.tweet_volume_24h = tvol24h

# end TrendSnapshot

