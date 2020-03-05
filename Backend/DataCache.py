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

    # TODO: Constructor takes a cache_max argument but is not yet implemented
    def __init__(self, cache_max=10):
        self.cache = {}
        self.cache_max = cache_max

    # Check if its a valid time to update the query in the cache
    # Add new query and results and return true if valid time
    # Return false if invalid time
    def add(self, query_string, result_string, mins=5):
        if self.should_update(query_string, mins):
            self.cache[query_string] = DataCacheResult(result_string, datetime.now())
            print("Cache updated query [", query_string, "]")
            return True
        else:
            return False

    # check if the query exist in the cache and was requested within <mins> minutes ago (default at 5 mins)
    # TRUE: if query was requested more than <mins> minutes ago
    # FALSE: if query was requested less than <mins> minutes ago
    def should_update(self, query_string, mins=5):
        if query_string in self.cache.keys():
            # if the query was previously called over <mins> minutes ago,
            if self.cache[query_string].get_timestamp() < (datetime.now() - timedelta(minutes=mins)):
                print("Query [", query_string, "] called over ", mins, " minute(s) ago. Ready to be locally updated.")
                return True
            else:
                print("Query [", query_string, "] called less than ", mins, " minute(s) ago.")
                return False
        else:
            print("Query [", query_string, "] does not exist. Ready to be locally cached.")
            return True

    # return the string result of the cached query
    # return None if query dont exist
    def retrieve(self, query_string):
        ret = None
        if self.has_key(query_string):
            ret = self.cache[query_string].get_result()
        return ret

    # return the string result of the cached query
    # return None if query dont exist
    # Also delete the query entry from the cache
    def remove(self, query_string):
        ret = None
        if self.has_key(query_string):
            ret = self.cache[query_string].get_result()
            del self.cache[query_string]
        return ret

    # Get the number of queries currently in cache
    def get_count(self):
        return len(self.cache)

    # Get the maximum number of queries that cache can store
    def get_max_length(self):
        return self.cache_max

    def has_key(self, key):
        return key in self.cache.keys()

