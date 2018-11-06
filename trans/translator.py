from functools import wraps
from collections import OrderedDict

def cache():
    def cache_decorator(fn):
        _cache = OrderedDict()
        @wraps(fn)
        def inner(*args, **kwargs):
            if args in _cache:
                print 'hit cache!'
                return _cache.get(args)
            print 'not hit', args
            r = fn(*args, **kwargs)
            return _cache.setdefault(args, r)

        return inner
    return cache_decorator

class BaseTranslator:
    def __init__(self, to_lang, from_lang, key=""):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.key = key
        self.cache = {}

    def translate(self, source):
        return source
