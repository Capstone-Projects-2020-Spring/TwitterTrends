from datetime import datetime, timedelta
import threading
import time

class TemporalDataManager:

    # TODO: set up instance of algorithm manager (and anything else needed)
    # TODO: tasked to set up threads that can access trends data retrieving functions
    def __init__(self,  algomanager, loc, t=3):
        self.algo = algomanager
        self.timer = t
        self.periodic_trends_on = True
        self.main_thread = threading.Thread(target=self.periodic_trends_retrieval, args=loc)
        print("STARTING TEMPORAL THREAD")
        self.main_thread.start()

    # TODO: this method will be periodically called by a thread
    # TODO: tasked to retrieve trends data and store them somewhere
    def periodic_trends_retrieval(self, *loc):
        while self.periodic_trends_on is True:
            print("Temporal: ", len(loc))
            time.sleep(30)  # sleep for seconds

    # TODO: periodically pull tweets at different dates
    # TODO: this method template is an oversight and it might not be necessary
    def periodic_tweets_retrieval(self):
        ()
