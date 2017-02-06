import datetime
import decorator
import shelve
from hashlib import md5

def scached(cache_file, expiry):
    def scached_closure(func, *args, **kw):
        key = md5(':'.join([func.__name__, str(args), str(kw)])).hexdigest()
        d = shelve.open(cache_file)

        # Expire old data if we have to
        if key in d:
            if d[key]['expires_on'] < datetime.datetime.now():
                del d[key]

        # Get new data if we have to
        if key not in d:
            print "Cache expired. Please wait while I retrieve fresh values... "
            data = func(*args, **kw)
            d[key] = {
                'expires_on' : datetime.datetime.now() + expiry,
                'data': data,
            }

        result = d[key]['data']
        d.close()

        return result

    return decorator.decorator(scached_closure)