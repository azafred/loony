from __future__ import print_function

import datetime
import os
import shelve
import sys
import time
from hashlib import md5

import boto
import decorator

from settings import *


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def scached(cache_file, expiry):
    def scached_closure(func, *args, **kw):
        key = md5(':'.join([func.__name__, str(args), str(kw)])).hexdigest()
        d = shelve.open(cache_file)
        changes = False

        # Expire old data if we have to
        if key in d:
            if d[key]['expires_on'] < datetime.datetime.now():
                del d[key]
            eprint("Cache set to expire on %s" % d[key]['expires_on'])
            eprint("Checking for changes...")
            dt_earlier = d[key]['expires_on'] - expiry
            earlier = time.mktime(dt_earlier.timetuple())
            stime = datetime.datetime.now()
            now = time.mktime(stime.timetuple())
            ct = boto.connect_cloudtrail()
            # print "earlier: %s - %s" % (earlier, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(earlier)))
            # print "now: %s - %s" % (now, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
            events = ct.lookup_events(start_time=earlier, end_time=now, lookup_attributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'RunInstances'}])['Events']
            for ev in events:
                ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ev['EventTime']))
                if 'ami' in ev['Resources'][0]['ResourceName']:
                    eprint(" !! Change detected: Instance: %s updated at %s" % (ev['Resources'][0]['ResourceName'], ts))
                    changes = True
        # Get new data if we have to
        if key not in d or changes:
            eprint("Please wait while I rebuild the cache... ")
            data = func(*args, **kw)
            d[key] = {
                'expires_on' : datetime.datetime.now() + expiry,
                'data': data,
            }

        result = d[key]['data']
        d.close()

        return result

    return decorator.decorator(scached_closure)

def expire_cache(cache_file=cache_file):
    try:
        cache_file = cache_file + ".db"
        os.remove(cache_file)
        eprint("Cache removed.")
    except:
        eprint("Something happened and I was not able to remove the cache file.")
        eprint("Please remove %s manually" % cache_file)
