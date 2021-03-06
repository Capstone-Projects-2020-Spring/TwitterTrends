from datetime import datetime, timedelta
import wrappers.geocode as geocode
from newsapi import NewsApiClient

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy
from PIL import Image

import os
from os import path

from DataCache import DataCache
from DatabaseRequester import DatabaseRequester
from TwitterAPIManager import TwitterAPIManager

from TemporalDataManager import TemporalDataManager

# from flask import jsonify # pronbably not needed
import DataStructures

import traceback

NEWS_API_KEY_ENV_VAR="NEWS_API_KEY"

# In charge of all algorithms needed by the backend server


class AlgorithmsManager:

    BASE_TREND_SNAPSHOTS_QUERY_TEMPLATE="SELECT * FROM trends_snapshot " \
                                        "\nWHERE created_date >= '{}' AND created_date < '{}' "

    FRIEND_NETWORK_TYPE= "friends"
    FOLLOWER_NETWORK_TYPE = "followers"


    def __init__(self, cache, db, twit):
        self.cache = cache
        self.database = db
        self.twitter = twit

        newsApiKeyVal = os.environ.get(NEWS_API_KEY_ENV_VAR)
        assert newsApiKeyVal != None, "News API Key environment variable not defined"
        self.news_api = NewsApiClient(api_key=newsApiKeyVal)

    # use the woeid argument to pull trends from Twitter API
    # pull results from cache if query was called recently
    # return top [num] trends
    # querystr argument is used for cache checking
    #       querystr must not be None
    def get_top_num_trends_from_location(self, woeid, num, sort=1, querystr=None, c_time = 5):

        if querystr is None:
            querystr = "/toptrends{}".format(woeid)

        cachetime = c_time # n minutes cache time check

        if self.cache.should_update(querystr, cachetime) or querystr is None:

            queryres = self.twitter.top_trends(woeid)  # api.trends_place(woeid)

            # Variables storing other info about the trends
            as_of = queryres['as_of']
            created_at = queryres['created_at']
            loc_name = queryres['locations'][0]['name']
            loc_woeid = queryres['locations'][0]['woeid']

            trends = []   # List of Trend objects
            i = 0
            for trend in queryres['trends']:
                vol = trend['tweet_volume']
                tempTrend = DataStructures.Trend(i,
                                                 trend['name'],
                                                 True if trend['name'][0] == '#' else False,
                                                 trend['query'],
                                                 vol)

                trends.append(tempTrend)
                i += 1

            # SORT the trends returned by the tweet volume
            # Sorting will ruin the true "local" trends.
            if sort == 1:
                print("SORTING TRENDS")
                AlgorithmsManager.sort_trends(trends)

            trends_n = []

            for k in range(0, min(num, len(trends))):
                trends_n.append(trends[k].__dict__)

            self.cache.add(querystr, trends, cachetime)
            return trends_n
        else:
            print("\nReturning [", querystr , "] from cache\n")
            trends = self.cache.retrieve(querystr)
            trends_n = []
            for k in range(0, min(num, len(trends))):
                trends_n.append(trends[k].__dict__)
            return trends_n
    # end get top trends from location

    # get a list of tweets from given query
    # return from cache if recently called
    # tweets time will be between timefrom->timeto
    # sort the list of tweets by retweet_count if sort == 1
    # return the number of tweets equal to specified num
    # optional Location object can be passed in
    # querystr is used for caching
    def get_top_tweets_from_query(self, query, num, location,
                                timefrom=datetime.now() - timedelta(days=5),
                                timeto=datetime.now(),
                                sort=1, querystr=None, c_time = 15):
        # Call a function from the TwitterAPIManager to return a list of tweets
        if querystr is None:
            querystr = "/toptweets{}{}-{}".format(query, location.latitude, location.longitude)

        cachetime = c_time # n minutes cache time check

        if self.cache.should_update(querystr, cachetime):

            # apitype 0 = standard 7 days
            # apitype 1 = premium 30 days
            apitype = 0 if timeto > datetime.now() - timedelta(days=7) else 1

            res = self.twitter.get_tweets(query, timefrom.strftime("%Y-%m-%d"),
                                                 timeto.strftime("%Y-%m-%d"),
                                          num, location, apitype=apitype)

            tweets = []  # list of Tweet object
            i = 0
            for tweet in res:
                # location object storing location data from the tweet json
                loc = DataStructures.Location(None, None, None, None, None, None, None)
                qcount = 0   # number of quotes
                rcount = 0   # number of replies
                url = None   # Tweets url
                # print(tweet)
                # TODO: need changes to all the locations values. probably isn't accurate right now
                if tweet['geo'] is not None:
                    if ('coordinates' in tweet['geo']) and tweet['geo']['coordinates']:
                        coord = tweet['geo']['coordinates']
                        loc = self.get_location_by_latlon(float(coord[0]), float(coord[1]))

                if 'quote_count' in tweet:
                    # store tweet['quote_count'] in qcount
                    qcount = tweet['quote_count']

                if 'reply_count' in tweet:
                    # store tweet['reply_count'] in rcount
                    rcount = tweet['reply_count']


                if 'entities' in tweet:
                    ents = tweet['entities']

                    if 'urls' in ents:
                        urls = ents['urls']
                        if len(urls) > 0:
                            url = urls[0]['expanded_url']


                # TODO: need changes to all the locations values. probably isn't accurate right now
                temptweet = DataStructures.Tweet(id=i,
                                                 ids=tweet['id'],
                                                 uid=tweet['user']['id'],
                                                 uname=tweet['user']['screen_name'],
                                                 cont=tweet['text'],
                                                 lat=loc.latitude, lon=loc.longitude, locid=loc.woeid, # location isfound in tweet['geo']
                                                 likes=tweet['favorite_count'],
                                                 quotes=qcount,
                                                 rtweets=tweet['retweet_count'],
                                                 repl=rcount,
                                                 date=tweet['created_at'],
                                                 url=url)
                tweets.append(temptweet)
                i += 1

            # SORT the tweets returned by the retweet_count
            # Sorting will ruin the true "local" trends.
            if sort == 1:
                print("SORTING TWEETS")
                AlgorithmsManager.sort_tweets(tweets)

            tweets_n = []
            for k in range(0, min(num, len(tweets))):
                tweets_n.append(tweets[k].__dict__)

            self.cache.add(querystr, tweets, cachetime)
            return tweets_n

        else:
            print("\nReturning [", querystr, "] from cache\n")
            tweets = self.cache.retrieve(querystr)
            tweets_n = []
            for k in range(0, min(num, len(tweets))):
                tweets_n.append(tweets[k].__dict__)
            return tweets_n
    # end get_top_tweets_from_query

    # method that find the length of the trends table from database
    def get_num_trends_from_database(self):
        dbqueryres = self.database.query("SELECT count(*) FROM trends;")
        print(dbqueryres.get_rows()[0][0])

    def get_highest_id_of_database_table(self, tablename, idname='id', default_id=0):
        dbqueryres = self.database.query("SELECT * FROM " + tablename + " ORDER BY " + idname + " DESC;")
        rows = dbqueryres.get_rows()
        colname = dbqueryres.get_column_names()
        lens = len(rows)
        if lens == 0:
            print("EMPTY TABLE. ID DEFAULT TO", default_id)
            return 0
        else:
            i = 0
            for n in colname:
                if n == idname:
                    highestid = rows[0][i]
                    print("HIGHEST ID FOR", tablename, ":", highestid)
                    return highestid
                i += 1


    # return a Location object
    # pass in an address string
    # Example addrstr: "1801 N Broad St, Philadelphia, PA 19122"
    def get_location_by_address(self, address):
        # TODO: possibly access database to check for existing location
        lat, lon = geocode.get_lat_lon_by_address(address)
        res = self.twitter.get_closest_location(lat, lon)
        return self.parse_location_json(res, lat, lon)

    # return a Location object
    # pass in latitude and longitude values
    # lat lon must be numeric strings or floats
    def get_location_by_latlon(self, lat, lon):
        # TODO: possibly access database to check for existing location
        res = self.twitter.get_closest_location(float(lat), float(lon))
        return self.parse_location_json(res, float(lat), float(lon))

    # take in a woeid and return a locations object
    def get_location_by_woeid(self, woeid):
        # TODO: possibly access the database here
        return {}

    def get_all_locations(self):

        # queryres row entry format:
        #     woe_id, city, states, lat, long
        queryres = self.database.query('SELECT * FROM locations;')
        resrows = queryres.get_rows()
        resarr = []
        for row in resrows:
            resarr.append(DataStructures.Location(row[0], row[1], row[2], None, row[0], row[3], row[4]).__dict__)
        return resarr

    def test(self):
        self.database.query("SELECT * FROM ")

    # parse the location json returned by twitter.get_closest_location
    # args:
    #   the json object
    #   the latitude and longitude of the location as floats
    def parse_location_json(self, loc, lat, lon):
        name = loc['name']
        parentid = loc['parentid']
        country = loc['country']
        woeid = loc['woeid']
        countryCode = loc['countryCode']

        location = DataStructures.Location(0, name, None, parentid, woeid, lat, lon)
        return location


    #retrieves news stories which reference the given trend
    # args:
    #   trend: the trend (keyword/phrase or hashtag) which should be searched for
    #   num_stories: the maximum number of stories about that trend to return
    def get_trend_news(self, trend, num_stories=3):
        stories_per_page=100
        if num_stories <= 0:
            raise ValueError("num_stories must be a positive value")
        elif num_stories <= 100:
            stories_per_page = num_stories
        else:
            print("WARN- the /trend_news endpoint doesn't yet support fetching over 100 stories at once")

        example_news_stories = []

        all_stories = self.news_api.get_everything(q=trend, language="en", page_size=stories_per_page)
        news_fetch_status = all_stories["status"]
        if news_fetch_status == "ok":
            stories_list = all_stories["articles"]
            num_fetched_stories = all_stories["totalResults"]

            for fetched_story in stories_list[:(min(num_stories, num_fetched_stories))]:
                example_story= {}
                example_story["title"] = fetched_story["title"]
                example_story["author"] = fetched_story["author"]
                example_story["source_name"] = fetched_story["source"]["name"]
                example_story["link_url"] = fetched_story["url"]
                example_story["date"] = fetched_story["publishedAt"]
                example_story["description"] = fetched_story["description"]
                example_story["content_start"] = fetched_story["content"]
                example_news_stories.append(example_story)
        else:
            example_news_stories.append("news api failed with error code " + all_stories["status"])

        #todo support fetching multiple pages of results for over 100 stories?
        return example_news_stories

    # TODO: this function adds a TrendSnapshot object to the database with proper format
    def add_trends_snapshot_to_database(self, snap):
        highid = self.get_highest_id_of_database_table('trends_snapshot', idname='id')

        querystr = "insert into trends_snapshot(id, woe_id, trend_content, query_term, tweet_volume, is_hashtag, created_date) values \n"

        i = 0
        trendlen = len(snap.trends)
        for trend in snap.trends:
            i += 1
            highid += 1

            querystr += "({}, {}, '{}', '{}', {}, {}, '{}')".format(highid,
                                                                    snap.woeid,
                                                                    trend['trend_content'].replace("%", "%%").replace("\'", "\'\'"),
                                                                    trend['query_term'].replace("%", "%%").replace("\'", "\'\'"),
                                                                    trend['tweet_volume'] if trend['tweet_volume'] is not None else 0,
                                                                    trend['is_hashtag'],
                                                                    snap.timestamp)  # we want to avoid single % symbol in sql queries
            if i != trendlen:
                querystr += ',\n'
            else:
                querystr += ';'

        print("Adding", trendlen, "trends to snapshot table")
        #print(querystr)
        self.database.query(querystr)

    def get_trends_snapshot_from_database(self, trends, fromdate, todate=datetime.now(), woeid=1):
        queryTemplate = AlgorithmsManager.BASE_TREND_SNAPSHOTS_QUERY_TEMPLATE + "\nAND trend_content = '{}' "

        # legacy query term checking query  # AND trend_content LIKE '%%{}%%'

        woeidQuery = ""
        if woeid != 1:
            woeidQuery = "AND woe_id = {} ".format(woeid)
        queryTemplate += woeidQuery
        queryTemplate += " ORDER BY created_date ASC;"

        snapsresultset = {}
        for trend in trends:
            trendalter = trend.replace("%", "%%")
            # todo I think this 4th argument to format shouldn't be needed or work at all because
            #  woeid was already formatted into woeidQuery & woeidQuery was just appended to queryTemplate
            querystr = queryTemplate.format(fromdate, todate, trendalter, woeidQuery)
            print(querystr)
            res = self.database.query(querystr)
            snapsresultset[trend] = res.get_rows()
        return snapsresultset


    def get_all_trends_with_snapshots(self, firstDate, lastDate, locationWoeid = None):
        """Fetches the database rows for all trend snapshots within the given timeframe and possibly in the given location

        Parameters:
            firstDate (datetime): beginning of timeframe
            lastDate (datetime): end of timeframe
            locationWoeid (int): which location the snapshots should be from; if None, then fetches snapshots from all locations

        Returns:
            list: rows from database
        """
        snapshotsQuery = AlgorithmsManager.BASE_TREND_SNAPSHOTS_QUERY_TEMPLATE.format(firstDate, lastDate)
        woeidQueryTerm = ""
        if locationWoeid != None:
            woeidQueryTerm = " AND woe_id = {} ".format(locationWoeid)
        snapshotsQuery += woeidQueryTerm
        snapshotsQuery += "\nORDER BY created_date ASC;"
        print(snapshotsQuery)

        queryResult = self.database.query(snapshotsQuery)
        snapshotRows = queryResult.get_rows()

        return snapshotRows


    # retrieves economic data for a state
    #   arg: state (full name)
    #   return type: a list of city data entry
    # city entry format: woe_id, city, state, lat, long, population, density, ranking, age_median
    #                   male, female, married, family_size, income_household_median, income_six_figure,
    #                   home_ownership, home_value, rent_median, education_college_or_above, 
    #                   labor_force_participation, unemployment_rate, race_white
    #                   race_black, race_asian, race_native, race_pacific, race_other, race_multiple
    def get_economic_data_by_state(self, state):
        queryres = self.database.query("SELECT * FROM all_city_social_data WHERE states = (%s);", state)
        resrows = queryres.get_rows()
        all_cities_data = []

        for entry in resrows:
            city = self.parse_city_data(entry, False)
            all_cities_data.append(city)

        return all_cities_data

    # retrieves economic data for a city
    #   arg: city (full name)
    #   return type: dict
    def get_economic_data_by_city(self, city):
        if city is not None:
            queryres = self.database.query("SELECT * FROM all_city_social_data WHERE city = (%s);", city)

        resrows = queryres.get_rows()
        city_data = self.parse_city_data(resrows[0], False)

        return city_data

    # retrieves economic data for a woeid
    #   arg: woeid (either str or int)
    #   return type: dict
    def get_economic_data_by_woeid(self, woeid):
       if woeid is not None:
            queryres = self.database.query("SELECT * FROM city_social_data WHERE woe_id = (%s);", woeid)

       resrows = queryres.get_rows()
       city_data = self.parse_city_data(resrows[0], True)

       return city_data


    # returns a city object (dict) for each city in the state
    # object contains socioeconomic data
    # adjusts column indices based on whether it's processing data from the older/smaller
    #table which has a woeid column or from the newer/larger table which doesn't
    def parse_city_data(self, entry, hasWoeid):
        city_data = {}

        if hasWoeid:
            city_data["woe_id"] = entry[1]
        indexAdjustment = 1 if hasWoeid else 0
        city_data["city"] = entry[1 + indexAdjustment]
        city_data["state"] = entry[2 + indexAdjustment]
        city_data["lat"] = entry[3 + indexAdjustment]
        city_data["long"] = entry[4 + indexAdjustment]
        city_data["population"] = entry[6 + indexAdjustment]
        city_data["density"] = entry[7 + indexAdjustment]
        city_data["ranking"] = entry[8 + indexAdjustment]
        city_data["age_median"] = entry[9 + indexAdjustment]
        city_data["male"] = entry[10 + indexAdjustment]
        city_data["female"] = entry[11 + indexAdjustment]
        city_data["married"] = entry[12 + indexAdjustment]
        city_data["family_size"] = entry[13 + indexAdjustment]
        city_data["income_household_median"] = entry[14 + indexAdjustment]
        city_data["income_six_figure_percent"] = entry[15 + indexAdjustment]
        city_data["home_ownership"] = entry[16 + indexAdjustment]
        city_data["home_value"] = entry[17 + indexAdjustment]
        city_data["rent_median"] = entry[18 + indexAdjustment]
        city_data["education_college_or_above"] = entry[19 + indexAdjustment]
        city_data["labor_force_participation"] = entry[20 + indexAdjustment]
        city_data["unemployment_rate"] = entry[21 + indexAdjustment]
        city_data["race_white"] = entry[22 + indexAdjustment]
        city_data["race_black"] = entry[23 + indexAdjustment]
        city_data["race_asian"] = entry[24 + indexAdjustment]
        city_data["race_native"] = entry[25 + indexAdjustment]
        city_data["race_pacific"] = entry[26 + indexAdjustment]
        city_data["race_other"] = entry[27 + indexAdjustment]
        city_data["race_multiple"] = entry[28 + indexAdjustment]

        return city_data
        
    def get_user_by_username(self, username):
        print("\nValidating user")
        try:
            ur = self.twitter.get_user(username)
            user = DataStructures.User(None, ur.id, ur.screen_name, ur.name, ur.created_at, ur.location,
                                        ur.protected, ur.followers_count, ur.friends_count)
            print("\nValidation success")
            return user.__dict__
        
        except:
            # TODO: A more general and reliably-accurate error message
            print("EXCEPTION: Fetching the description of a user failed")
            return None

    # this function returns a dictionary of retweeters
    #   args:   username
    #           num_tweets (optional): how many recent tweets to search through
    #           num_retweets (optional): how many retweeters per tweet
    #   return: a dictionary
    def get_most_frequent_retweeters(self, username, num_tweets=20, num_retweets=20):

        retweetData = self.twitter.most_recent_retweeters(username, num_tweets=num_tweets, num_retweets=num_retweets)
        
        # get the list of all retweeters
        retweeter_history = []
        for tweet in retweetData:
            innerList = tweet['retweeters']
            for username in innerList:
                retweeter_history.append(username)

        # count the number of retweets
        res = {}
        for user_id in retweeter_history:
            if res.get(user_id) is None:
                res[user_id] = 1
            else:
                res[user_id] += 1

        return res

    def get_network_tweets_text(self, id2, username, count, depth, network_type):
        textsStr = ""
        if id2 > 0 or username is not None:
            # get bunch of tweets starting with the user of given id
            n = depth  # goes depth level deep
            # array of tweet texts
            texts = []
            self.append_texts_recursive(texts, count, n, 0, id2, username, network_type)

            for text in texts:
                splittext = text.split(' ')
                for split in splittext:
                    if not split.startswith('http'):
                        textsStr += (split + " ")
        return textsStr

    def append_texts_recursive(self, texts, count, n, i, id2, username, network_type):
        tweets = self.twitter.getTweetsFromUser(id2, username, count)
        for text in tweets:
            texts.append(text)
        if i < n:
            otherUserIds = []
            if network_type == AlgorithmsManager.FRIEND_NETWORK_TYPE:
                otherUserIds = self.twitter.getFriendsID(id2, username, count)
            elif network_type == AlgorithmsManager.FOLLOWER_NETWORK_TYPE:
                otherUserIds = self.twitter.getFollowersID(id2, username, count)
            else:
                raise ValueError("invalid network type " + network_type)

            for id3 in otherUserIds:
                screen_name = self.twitter.get_username_from_id(id3)
                self.append_texts_recursive(texts, n, count, i+1, id3, screen_name, network_type)

    def create_wordcloud_image(self, network_type, id2=0, username=None, count=5, depth=1, querystr=None, c_time = 15):
        if querystr is None:
            querystr = "/wordcloud{}{}{}".format(network_type, id2, username)

        cachetime = c_time  # n minutes cache time check

        if self.cache.should_update(querystr, cachetime):
            words = self.get_network_tweets_text(id2, username, count, depth, network_type)
            if words != "":
                workingdir = os.path.dirname(__file__)
                stopwords = set(STOPWORDS)
                stopwords.add('RT')
                stopwords.add('https')
                maskfilename = "wordcloud/mask.png"
                cloudfilename = "wordcloud/cloud.png"
                mask = numpy.array(Image.open(os.path.join(workingdir, maskfilename)))
                cloud = WordCloud(background_color="white", mask=mask, stopwords=stopwords)
                cloud.generate(words)
                cloud.to_file(os.path.join(workingdir, cloudfilename))
                if path.exists(os.path.join(workingdir, cloudfilename)):
                    returnPath = os.path.join(workingdir, cloudfilename)
                    self.cache.add(querystr, returnPath, cachetime)
                    return returnPath
                else:
                    return None
            else:
                return None
        else:
            print("\nReturning [", querystr, "] from cache\n")
            words = self.cache.retrieve(querystr)
            return words

    # pass in array of Trend object and this will sort it using insertion sort
    @staticmethod
    def sort_trends(arr):
        length = len(arr)
        for l in range(1, length):
            temp = arr[l]
            tempval = temp.tweet_volume
            k = l-1

            num_trend_sort_iter = 0

            while k >= 0 and    (tempval if tempval is not None else 0) >= \
                                (arr[k].tweet_volume if arr[k].tweet_volume is not None else 0):
                arr[k+1] = arr[k]
                k -= 1

                # todo strip debugging code from while loop
                num_trend_sort_iter +=1
                if num_trend_sort_iter >= 10000:
                    print("while loop started to go infinite:\nARGUMENTS:\n",
                          "arr= ", arr,
                          ";\n\nVARIABLES:\n",
                          "temp= ", temp, "\ntempval= ", tempval, "\nk= ", k,
                          "\nSTACK TRACE:\n")

                    traceback.print_stack()
                    raise Exception("got into infinite loop")

            arr[k+1] = temp


    # pass in array of Tweet object and this will sort it using insertion sort
    @staticmethod
    def sort_tweets(arr):
        length = len(arr)
        for l in range(1, length):
            temp = arr[l]
            tempval = temp.retweets
            k = l - 1

            num_tweet_sort_iter = 0

            while k >= 0 and (tempval if tempval is not None else 0) >= \
                    (arr[k].retweets if arr[k].retweets is not None else 0):
                arr[k + 1] = arr[k]
                k -= 1

                #todo strip debugging code from while loop
                num_tweet_sort_iter += 1
                if num_tweet_sort_iter >= 10000:
                    print("while loop started to go infinite:\nARGUMENTS:\n",
                          "arr= ", arr,
                          ";\n\nVARIABLES:\n",
                          "temp= ", temp, "\ntempval= ", tempval, "\nk= ", k,
                          "\nSTACK TRACE:\n")

                    traceback.print_stack()
                    raise Exception("got into infinite loop")


            arr[k + 1] = temp

    # pass in a dictionary and the length of the returned shortlist
    # return a list of tuples, sorted by the retweet count
    @staticmethod
    def list_top_retweeters(dict, count):
        sorted_list = []
        keyList = list(dict)

        for k in range(count):
            temp_key = keyList[0]
            temp_val = dict[temp_key]
            for iter_key in keyList:
                if dict[iter_key] >= temp_val:
                    temp_key = iter_key
                    temp_val = dict[iter_key]
            
            user = {"username": temp_key, "retweet_count": temp_val}
            sorted_list.append(user)
            dict[temp_key] = -1

        return sorted_list

    # create a bucket grouped by date from an array of trendssnapshot tuples from database query
    # array element format: id, woe_id, trend_content, query_term, tweet_volume, is_hashtag, created_date
    @staticmethod
    def get_snapstime_bucket_from_database_tuples(snaps, starttime, endtime, days=0, hours=2, minutes=0, seconds=0):
        snapslen = len(snaps)
        tempbucket = {}

        if snapslen > 0:
            curtime = starttime
            tempbucket[curtime] = []
            for snap in snaps:
                d = snap[TemporalDataManager.SNAPSHOT_DATE_COLUMN_INDEX]
                dcap = curtime + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

                num_bucket_cap_search_iter = 0

                while d >= dcap and d <= endtime:
                    if len(tempbucket[curtime]) == 0:
                        del tempbucket[curtime]
                    curtime = dcap
                    dcap = curtime + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
                    tempbucket[curtime] = []

                    # todo strip debugging code from while loop
                    num_bucket_cap_search_iter += 1
                    if num_bucket_cap_search_iter >= 10000:
                        print("while loop started to go infinite:\nARGUMENTS:\n",
                              "snaps= ", snaps, "\nstarttime= ", starttime, "\nendtime= ", endtime,
                              "\n\ndays= ", days, "\nhours= ", hours, "\nminutes= ", minutes, "\nseconds= ", seconds,
                              ";\n\nVARIABLES:\n",
                              "tempbucket= ", tempbucket, "\ncurtime= ", curtime, "\nsnap= ", snap,
                              "\nd= ", d, "\ndcap= ", dcap,
                              "\nSTACK TRACE:\n")

                        traceback.print_stack()
                        raise Exception("got into infinite loop")

                tempbucket[curtime].append(snap)

        return tempbucket



    # function that takes two strings and return an HTML text in a format like:
    #       REQUIRED
    #       [arg1]
    #       [arg2]
    #
    #       optional
    #       [arg1]
    #       [arg2]
    @staticmethod
    def get_args_as_html_str(required, optional):
        htmlstr = ""
        if len(required) > 0:
            htmlstr += "<b>REQUIRED</b><br>"
            for arg in required:
                htmlstr += "["+arg+"]<br>"
            htmlstr += "<br>"
        if len(optional) > 0:
            htmlstr += "<i><b>optional</b></i><br>"
            for arg in optional:
                htmlstr += "["+arg+"]<br>"
        return htmlstr

if __name__ == "__main__":
    #algos = AlgorithmsManager(None, None, None)
    #print(algos.get_trend_news("tacos"))

    # SETUP DataCache
    cache = DataCache()

    # SETUP DatabaseRequester
    db = DatabaseRequester( host="twittertrends.cmxd9oibzmhi.us-east-2.rds.amazonaws.com",
                        port="5432",
                        database="postgres",
                        user="master_user",
                        password="ULllhejK2ykYroghntj0"
    )

    # SETUP TwitterAPIManager
    twitter = TwitterAPIManager()

    # SETUP AlgorithmsManager
    algo = AlgorithmsManager(cache, db, twitter)

    username = "MSNBC"

    res = algo.get_most_frequent_retweeters(username, num_tweets=20, num_retweets=20)
    # print(res)

    sortedList = algo.list_top_retweeters(res, 10)
    print(sortedList)
