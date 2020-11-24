import collections
import logging


__logger__ = logging.getLogger(__name__)


class CacheRecent(object):
    def __init__(self, limit=512):
        self.__limit = limit
        self.__cache = collections.OrderedDict()

    def __setitem__(self, param_key, param_value):
        # Existing value?
        #
        if param_key in self.__cache:
            # Update insertion order
            #
            del self.__cache[param_key]
        elif len(self.__cache) >= self.__limit:
            # Delete oldest items
            #
            keys = self.__cache.keys()
            half_limit = self.__limit / 2
            half_keys = keys[:half_limit]
            for key in half_keys:
                del self.__cache[key]

        # Insert entry
        #
        self.__cache[param_key] = param_value

    def __getitem__(self, param_key):
        # Update insertion order
        #
        if param_key in self.__cache:
            value = self.__cache[param_key]
            del self.__cache[param_key]
            self.__cache[param_key] = value

        result = self.__cache[param_key]

        return result

    def __delitem__(self, param_key):
        del self.__cache[param_key]

    def __contains__(self, param_key):
        result = param_key in self.__cache

        return result

    def keys(self):
        return self.__cache.keys()

    def items(self):
        return self.__cache.items()

    def iteritems(self):
        return self.__cache.iteritems()

    def dump(self):
        for x, y in self.__cache.iteritems():
            print(f"{x}: {y}")
