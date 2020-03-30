from datetime import datetime, timedelta
import threading
import time
import DataStructures

class TemporalDataManager:

    # TODO: set up instance of algorithm manager (and anything else needed)
    # TODO: tasked to set up threads that can access trends data retrieving functions
    def __init__(self,  algomanager, t=24):
        self.algo = algomanager
        self.timer = t
        self.periodic_trends_on = True
        self.locations = self.algo.get_all_locations()
        self.timestamps = []
        self.main_thread = threading.Thread(target=self.periodic_trends_retrieval)
        print("STARTING TEMPORAL THREAD")
        self.testval = 0
        #self.main_thread.start()

# continue here
    # this method will be periodically called by a thread
    # tasked to retrieve trends data and store them somewhere
    # call functions to store snapshot entries in trends_snapshot databae table
    #       table trends_snapshots(id, woe_id, trend_content, query_term, tweet_volume, is_hashtag, created_date)
    def periodic_trends_retrieval(self):
        while self.periodic_trends_on is True:
            timestamp = datetime.now()
            snapid = 0
            for loc in self.locations:
                restrends = self.algo.get_top_num_trends_from_location(int(loc['woeid']), 50)
                print('TEMPORAL GET ', loc['woeid'])
                snap = DataStructures.TrendsSnapshot.create_trends_snapshot(snapid, restrends, loc, timestamp)

                self.algo.add_trends_snapshot_to_database(snap)

                # print(snap.__dict__)
                snapid += 1
                time.sleep(self.timer)   # sleep for 24 seconds to avoid Twitter get/trends rate limit

            time.sleep(9000) # sleep for 2.5 hours (9000 seconds)

    # TODO: periodically pull tweets at different dates
    # TODO: this method template is an oversight and it might not be necessary
    def periodic_tweets_retrieval(self):
        ()

    #       get the timeline of the trend. Return all occurrences of the trend given a datetime span
    #       trend: the trend keyword
    #       woeid: the location of the trend.
    #       fromdate: the datetime to search from
    #       todate: the datetime to search to
    #       days, hours, minutes, seconds = the time step of each unit
    #       return value: return a csv format string in format:  datetime,val1,val2,val3
    def get_trends_snapshot_as_csv(self, trends, fromdate, todate, woeid=1, days=0, hours=2, minutes=0, seconds=0):
        # call algo manager to query to database and return trends within the time frame
        # snapres return an array of database request for trend_snapshot data
        # each element are for each trend in the trends argument
        snapsres = self.algo.get_trends_snapshot_from_database(trends, fromdate, todate, woeid)

        # preload the precv dictionary
        precsv = {}             # dictionary to be parsed into csv. contain date key and array of tweet volume values
        numTrendsRequested = len(trends)   # max amount of value for each dictionary entry
        tempdate = fromdate
        while tempdate < todate:
            precsv[tempdate] = []
            tempdate += timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        for dateentry in precsv:
            for i in range(numTrendsRequested):
                precsv[dateentry].append(0)

        i = 0
        # queryTrend represent each term in the [trends] argument
        for queryTrend in snapsres.keys():
            rows = snapsres[queryTrend]
            lenrows = len(rows)

            print("Snapshots retrieved for {}: {}".format(trends[i], lenrows))

            snapsbucket = self.algo.get_snapstime_bucket_from_database_tuples(rows, fromdate, days=days, hours=hours, minutes=minutes, seconds=seconds)
            prevval = 0
            for date in snapsbucket.keys():
                snaps = snapsbucket[date]
                totalvol = 0
                for snap in snaps:
                    totalvol += snap[4]
                precsv[date][i] = totalvol    # updating the tweet volume value normally with just totalvol

                # code comment below is for saving previous totalvol value.
                # if new value is 0 then reuse the previous totalvol value
                """
                if totalvol == 0:
                    precsv[date][i] = prevval
                else:
                    precsv[date][i] = totalvol
                    prevval = totalvol
                """
            i += 1  # increment the trend index
            print()

        # create csv format string  datetime,val1,val2,val3....  to return to front end for grapahing
        #       format: datetime,v1,v2,v3
        #               datetime,v1,v2,v3

        csv = "datetime, "
        for i in range(numTrendsRequested):
            csv += "trend{}".format(i)
            if i != numTrendsRequested-1:
                csv += ", "
        csv += "\n"

        for key in precsv:
            csv += "{}, ".format(key)

            vals = precsv[key]
            valcounter = 0
            for val in vals:
                valcounter += 1
                csv += str(val)
                if valcounter != numTrendsRequested:
                    csv += ", "

            csv += "\n"

        print(csv)
        return csv
