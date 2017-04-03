#!/usr/bin/env python


import argparse
import logging
import __builtin__
import sys
from aws_fetcher import aws_inventory, list_keys
from display import display_results_ordered
from search import searchfor
from connect import connect_to
from cache import expire_cache
from settings import *
from version import __version__

def connect():
    main(connect=True, running_only=True)

def main(connect=False, running_only=True):

    parser = argparse.ArgumentParser(description='Find stuff in AWS')
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='Increase log verbosity', dest='verbose')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='Debug level verbosity', dest='debug')
    parser.add_argument(
        '--short', action='store_true', default=False,
        help='Display short-format results', dest='short')
    parser.add_argument(
        '--long', action='store_true', default=False,
        help='Display long-format results', dest='long')
    parser.add_argument(
        '--nocache', action='store_true', default=False,
        help='Force cache expiration', dest='nocache')
    parser.add_argument(
        '-k', '--keys', action='store_true', default=False,
        help="List all the keys for indexing or output", dest='listkeys')
    parser.add_argument(
        '--version', action='store_true', default=False,
        help="Print version", dest='version')
    parser.add_argument(
        '-o', '--out', type=str, nargs='?',
        help='Output format eg. id,name,pub_ip', dest='output')
    parser.add_argument(
        '-u', '--user', type=str, nargs='?',
        help='When connecting, what user to ssh in as', dest='user')
    parser.add_argument(
        '-c', '--connect', action='store_true',
        default=False,
        help="Connect to one or more instances",
        dest='connectcli')
    parser.add_argument(
        'search', metavar='search', type=str, nargs='*',
        help='Search parameters')

    args = parser.parse_args()
    global verbose
    __builtin__.verbose = args.verbose
    __builtin__.debug = args.debug
    __builtin__.stopped = False
    __builtin__.running = running_only
    __builtin__.short = args.short
    __builtin__.long = args.long
    if args.output:
        output = args.output.split(',')
        __builtin__.output = output
    else:
        __builtin__.output = prefered_output
    search = args.search
    nocache = args.nocache
    version = args.version
    listkeys = args.listkeys
    connectcli = args.connectcli
    user = args.user
    if version:
        show_version()
        sys.exit(0)
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    if nocache:
        expire_cache()
    if listkeys:
        list_keys()
    elif search:
        print "Searching for %s" % search
        results = searchfor(search)
        if connect or connectcli:
            if user:
                connect_to(results, user)
            else:
                connect_to(results)

    else:
        instances = aws_inventory(create_index=True)
        display_results_ordered(instances)

def show_version():
    print "Loony version %s " % __version__


if __name__ == '__main__':
    main()
