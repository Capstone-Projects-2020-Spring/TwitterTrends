from datetime import datetime, timedelta


# data class for the string result and timestamp of a query
class DataCacheResult:

    def __init__(self, result_string, timestamp):
        self.result = result_string
        self.timestamp = timestamp

    def get_result(self):
        return self.result

    def get_timestamp(self):
        return self.timestamp


class DataCache:

    def __init__(self):
        self.cache = {}

    def add(self, query_string, result_string, mins=5):
        if self.should_update(query_string, mins):
            self.cache[query_string] = DataCacheResult(result_string, datetime.now())
            return True
        else:
            return False

    # check if the query was requested within <mins> minutes ago (default at 5 mins)
    # TRUE: if query was requested more than <mins> minutes ago
    # FALSE: if query was requested less than <mins> minutes ago
    def should_update(self, query_string, mins=5):
        if query_string in self.cache.keys():
            # if the query was previously called over 5 minutes ago,
            if self.cache[query_string].get_timestamp() < (datetime.now() - timedelta(minutes=mins)):
                print("More than 5")
                return True
            else:
                print("Less than 5")
                return False
        else:
            print("Query does not exist")
            return True

    def retrieve(self, query_string):
        ret = None
        if self.has_key(query_string):
            ret = self.cache[query_string].get_result()
        return ret

    def remove(self, query_string):
        ret = None
        if self.has_key(query_string):
            ret = self.cache[query_string].get_result()
            del self.cache[query_string]
        return ret

    def get_count(self):
        return len(self.cache)

    def get_length(self):
        return len(self.cache)

    def has_key(self, key):
        return key in self.cache.keys()

