from datetime import datetime, timedelta
import threading
import time
import DataStructures

import traceback
import numpy as np
from collections import OrderedDict

class TemporalDataManager:
    SNAPSHOT_WOEID_COLUMN_INDEX = 1
    SNAPSHOT_TREND_CONTENT_COLUMN_INDEX = 2
    SNAPSHOT_TWEET_VOLUME_COLUMN_INDEX = 4
    SNAPSHOT_DATE_COLUMN_INDEX = 6

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
        self.main_thread.start()

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

        num_tempdate_find_iter = 0

        while tempdate < todate:
            precsv[tempdate] = []
            tempdate += timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

            # todo strip debugging code from while loop
            num_tempdate_find_iter += 1
            if num_tempdate_find_iter > 10000:
                print("while loop started to go infinite:\nARGUMENTS:\n",
                      "trends= ", trends, "\nfromdate= ", fromdate, "\ntodate= ", todate,
                      ";\n woeid= ", woeid, "\ndays= ", days, "\nhours= ", hours, "\nminutes= ", minutes, "\nseconds= ", seconds,
                      ";\n\nVARIABLES:\n",
                      "snapsres= ", snapsres, "\nprecsv= ", precsv, "\ntempdate= ", tempdate,
                      "\nSTACK TRACE:\n")

                traceback.print_stack()
                raise Exception("got into infinite loop")

        for dateentry in precsv:
            for i in range(numTrendsRequested):
                precsv[dateentry].append(0)

        i = 0
        # queryTrend represent each term in the [trends] argument
        for queryTrend in snapsres.keys():
            rows = snapsres[queryTrend]
            lenrows = len(rows)

            print("Snapshots retrieved for {}: {}".format(trends[i], lenrows))

            snapsbucket = self.algo.get_snapstime_bucket_from_database_tuples(rows, fromdate, todate, days=days, hours=hours, minutes=minutes, seconds=seconds)
            prevval = 0
            for date in snapsbucket.keys():
                snaps = snapsbucket[date]
                totalvol = 0
                maxvol = 0
                for snap in snaps:
                    totalvol += snap[4]

                    # storing extra value for maximum volume in the tweet_volume set
                    if snap[4] > maxvol:
                        maxvol = snap[4]
                precsv[date][i] = int(totalvol/len(snaps))   # Update using AVERAGE tweet volume value instead

            i += 1  # increment the trend index
            print()

        # create csv format string  datetime,val1,val2,val3....  to return to front end for grapahing
        #       format: datetime,v1,v2,v3
        #               datetime,v1,v2,v3

        csv = "datetime,"
        for i in range(numTrendsRequested):
            csv += trends[i]
            if i != numTrendsRequested-1:
                csv += ","
        csv += "\n"

        prevval = [0] * numTrendsRequested
        for key in precsv:
            csv += "{},".format(key)

            vals = precsv[key]
            valcounter = 0
            for val in vals:
                newval = val
                if val == 0:
                    newval = prevval[valcounter]
                prevval[valcounter] = newval
                csv += str(newval)
                valcounter += 1
                if valcounter != numTrendsRequested:
                    csv += ","

            csv += "\n"

        print(csv)
        return csv

    def collect_trend_history_options(self, initDate, finalDate, locationId= None):
        """assembles a summary of the trends that were popular at one or more times
        Only looks within a given period and possibly only in one location

        Parameters:
            initDate (datetime): beginning of time window to look for snapshots in
            finalDate (datetime): end of time window to look for snapshots in
            locationId (int): woeid of a location which the snapshots should be from

        Returns:
            list: a list of dictionaries, where each dict summarizes the history of a trend's popularity within the
            given window
            Note- this dictionary should be ordered so that a trend whose first moment of popularity was earlier
            would be listed before a trend whose first moment of popularity was later
        """

        snapshots = self.algo.get_all_trends_with_snapshots(initDate, finalDate, locationId)

        trendContentLabel = "trend_content"
        maxTweetVolumeLabel = "max_tweet_volume"
        avgTweetVolumeLabel = "avg_tweet_volume"

        firstDateLabel = "first_date"
        lastDateLabel = "last_date"
        locationsLabel = "locations"
        tweetVolumesLabel = "tweet_volumes"

        historicalTrends = OrderedDict()

        for trendSnap in snapshots:
            snapWoeid = trendSnap[TemporalDataManager.SNAPSHOT_WOEID_COLUMN_INDEX]
            snapTrend = trendSnap[TemporalDataManager.SNAPSHOT_TREND_CONTENT_COLUMN_INDEX]
            snapTweetVol = trendSnap[TemporalDataManager.SNAPSHOT_TWEET_VOLUME_COLUMN_INDEX]
            snapDate = trendSnap[TemporalDataManager.SNAPSHOT_DATE_COLUMN_INDEX]

            if snapTrend not in historicalTrends:
                historicalTrends[snapTrend] = \
                    {firstDateLabel:snapDate, lastDateLabel: snapDate, locationsLabel: {snapWoeid},
                     tweetVolumesLabel:[]}
            else:
                prevEarliestDate = historicalTrends[snapTrend][firstDateLabel]
                if prevEarliestDate > snapDate:
                    historicalTrends[snapTrend][firstDateLabel] = snapDate

                prevLatestDate = historicalTrends[snapTrend][lastDateLabel]
                if prevLatestDate < snapDate:
                    historicalTrends[snapTrend][lastDateLabel] = snapDate

                historicalTrends[snapTrend][locationsLabel].add(snapWoeid)

            if snapTweetVol > 0:
                historicalTrends[snapTrend][tweetVolumesLabel].append(snapTweetVol)

        historicalTrendsSummary = []

        for histTrend, trendDetails in historicalTrends.items():
            trendTweetVolumes = trendDetails[tweetVolumesLabel]
            maxTweetVol = 0
            avgTweetVol = 0
            if len(trendTweetVolumes) > 0:
                maxTweetVol = int(np.max(trendTweetVolumes))
                avgTweetVol = float(np.average(trendTweetVolumes))

            trendLocations = list(trendDetails[locationsLabel])
            trendEarliestDate = trendDetails[firstDateLabel].isoformat()
            trendLatestDate = trendDetails[lastDateLabel].isoformat()

            trendSummary = {trendContentLabel:histTrend, firstDateLabel:trendEarliestDate,
                            lastDateLabel:trendLatestDate, maxTweetVolumeLabel:maxTweetVol,
                            avgTweetVolumeLabel:avgTweetVol, locationsLabel:trendLocations}
            historicalTrendsSummary.append(trendSummary)


        return historicalTrendsSummary

