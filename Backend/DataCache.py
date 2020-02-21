
# TODO: implement a way to limit the cache size with a circular cache

class DataCache:

    cache = None
    cache_index = None
    cache_max = None

    def __init__(self, cache_max=20):
        self.cache = {}
        self.cache_index = 0
        self.cache_max = cache_max

    def add(self, query_string, result_string):
        self.cache[query_string] = result_string

    def retrieve(self, query_string):
        ret = None
        if self.has_key(query_string):
            ret = self.cache[query_string]
        return ret

    def remove(self, query_string):
        ret = None
        if self.has_key(query_string):
            ret = self.cache[query_string]
            del self.cache[query_string]
        return ret

    def get_count(self):
        return len(self.cache)

    def get_length(self):
        return len(self.cache)

    def has_key(self, key):
        return key in self.cache.keys()