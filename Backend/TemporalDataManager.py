from datetime import datetime
import threading
import time

class TemporalDataManager:

    # TODO: set up instance of algorithm manager (and anything else needed)
    # TODO: tasked to set up threads that can access trends data retrieving functions
    def __init__(self,  algomanager, loc, t=3):
        self.algo = algomanager
        self.timer = t
        self.periodic_trends_on = True
        self.timestamps = []
        self.main_thread = threading.Thread(target=self.periodic_trends_retrieval, args=loc)
        print("STARTING TEMPORAL THREAD")
        self.testval = 0
        #self.main_thread.start()

# continue here
    # TODO: this method will be periodically called by a thread
    # TODO: tasked to retrieve trends data and store them somewhere
    # TODO: call functions to store snapshot entries in trends_snapshot databae table
    #       table trends_snapshots(id, woe_id, trend_content, query_term, tweet_volume, is_hashtag, created_date)
    def periodic_trends_retrieval(self, *loc):
        while self.periodic_trends_on is True:
            timestamp = datetime.now()
            snapid = 0
            locations = self.algo.get_all_locations()
            for loc in locations:
                restrends = self.algo.get_top_num_trends_from_location(int(loc['woeid']), 50)
                print('TEMPORAL GET ', loc['woeid'])
                snap = self.algo.create_trends_snapshot(snapid, restrends, loc, timestamp)

                self.algo.add_trends_snapshot_to_database(snap)

                # print(snap.__dict__)
                snapid += 1
                time.sleep(24)   # sleep for 24 seconds to avoid Twitter get/trends rate limit

    # TODO: periodically pull tweets at different dates
    # TODO: this method template is an oversight and it might not be necessary
    def periodic_tweets_retrieval(self):
        ()

    # TODO: get the timeline of the trend. Return all occurrences of the trend at a location between a datetime
    #       trend: the trend keyword
    #       woeid: the location of the trend
    #       fromdate: the datetime to search from
    #       todate: the datetime to search to
    #       return value: return an array of Trends with each having a timestamp value
    def get_trends_snapshot(self, trends, fromdate, todate, woeid=0):
        # call algo manager to query to database and return trends within the time frame
        snapsres = self.algo.get_trends_snapshot_from_database(trends, fromdate, todate, woeid)
        rows = snapsres.get_rows()
        lenrows = snapsres.rows_count()

        print("Snapshots retrieved:", lenrows)

        # return a bucket with time and array of snaps within the same timestamp
        snapsbucket = self.algo.get_snapstime_bucket_from_database_tuples(rows, fromdate, days=0, hours=0, minutes=0, seconds=5)
        for date in snapsbucket.keys():
            snaps = snapsbucket[date]
            print(date, len(snapsbucket[date]))



        # TODO: create csv format string  datetime,val1,val2,val3....  to return to front end for grapahing
        csv = "test,test1,test2"

        return csv
