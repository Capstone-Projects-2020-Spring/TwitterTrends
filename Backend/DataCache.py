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

    def add(self, query_string, result_string):
        if query_string in self.cache.keys():
            if self.cache[query_string].get_timestamp() < (datetime.now() - timedelta(minutes=5)):
                self.cache[query_string] = DataCacheResult(result_string, datetime.now())
                print("CACHE NEW TIMESTAMP FOR ", "[", query_string, "]")
            else:
                print("CACHE ERROR ADD TOO QUICKLY ", "[",query_string, "]")
        else:
            print("CACHE NEW ENTRY ", "[", query_string, "]")
            self.cache[query_string] = DataCacheResult(result_string, datetime.now())

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

