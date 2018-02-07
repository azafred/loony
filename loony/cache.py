from __future__ import print_function

import datetime
import os
import shelve
import dbm
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
        try:
            d = shelve.open(cache_file)
            changes = False
        except:
            expire_cache(cache_file=cache_file)
            changes = True
            d = shelve.open(cache_file)

        # Expire old data if we have to
        try:
            if key in d:
                if d[key].get('expires_on', datetime.datetime.now()) < datetime.datetime.now():
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
                if not changes:
                    eprint("No changes detected. Using cache.")
            # Get new data if we have to
            if key not in d or changes:
                eprint("Please wait while I rebuild the cache... ")
                data = func(*args, **kw)
                d[key] = {
                    'expires_on' : datetime.datetime.now() + expiry,
                    'data': data,
                }

            result = d[key].get('data', '')
            if not result:
                result = scached(cache_file, expiry)
            d.close()
            return result
        except Exception as e:
            eprint("Debug: Problem with cache: {}".format(str(e)))
            expire_cache(cache_file=cache_file)
            pass
    return decorator.decorator(scached_closure)


def expire_cache(cache_file=cache_file):
    try:
        cache_file = cache_file
        os.remove(cache_file)
        eprint("Cache removed.")
    except Exception as e:
        try:
            cache_file = cache_file + ".db"
            os.remove(cache_file)
        except Exception as f:
            eprint("Debug: Removing cache file: {}".format(str(e) + str(f)))
            pass
