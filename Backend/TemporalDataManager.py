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
        self.main_thread.start()

    # TODO: this method will be periodically called by a thread
    # TODO: tasked to retrieve trends data and store them somewhere
    def periodic_trends_retrieval(self, *loc):
        while self.periodic_trends_on is True:
            #self.algo.get_num_trends_from_database()
            timestamp = datetime.now()
            snapid = 0
            locations = self.algo.get_all_locations()
            for loc in locations:
                restrends = self.algo.get_top_num_trends_from_location(int(loc['woeid']), 50)
                print('TEMPORAL GET ', loc['woeid'])
                snap = self.algo.create_trends_snapshot(snapid, restrends, loc, timestamp)
                print(snap.__dict__)
                snapid += 1
                time.sleep(24)   # sleep for 24 seconds to avoid Twitter get/trends rate limit

    # TODO: periodically pull tweets at different dates
    # TODO: this method template is an oversight and it might not be necessary
    def periodic_tweets_retrieval(self):
        ()
