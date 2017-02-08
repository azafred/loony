#!/usr/bin/env python


import argparse
import logging
import __builtin__
import sys
from aws_fetcher import aws_inventory
from display import display_results_ordered, test
from search import searchfor, pub_ip
from connect import connect_to
from cache import expire_cache
from settings import *
from version import __version__

def connect():
    main(connect=True, running_only=True)

def main(connect=False, running_only=False):

    parser = argparse.ArgumentParser(description='Find stuff in AWS')
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='Increase log verbosity', dest='verbose')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='Debug level verbosity', dest='debug')
    parser.add_argument(
        '-la', '--list-all', action='store_true', default=False,
        help='List all instances', dest='listall')
    parser.add_argument(
        '-so', '--stopped', action='store_true', default=False,
        help='Only display stopped instances', dest='stopped')
    parser.add_argument(
        '-ro', '--running', action='store_true', default=False,
        help='Only display running instances', dest='running')
    parser.add_argument(
        '-pub', '--public', action='store_true', default=False,
        help='Find those instances with public IPs', dest='public')
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
        '--or', action='store_true', default=False,
        help='Search item OR instead of combined', dest='oroperand')
    parser.add_argument(
        '--version', action='store_true', default=False,
        help="Print version", dest='version')
    parser.add_argument(
        '--test', action='store_true', default=False,
        help="test", dest='testnstuff')
    parser.add_argument(
        '-o', '--out', type=str, nargs='?',
        help='Output format eg. id,name,pub_ip', dest='output')
    parser.add_argument(
        'search', metavar='search', type=str, nargs='*',
        help='Search parameters')

    args = parser.parse_args()
    global verbose
    __builtin__.verbose = args.verbose
    __builtin__.debug = args.debug
    __builtin__.stopped = args.stopped
    __builtin__.running = args.running or running_only
    __builtin__.short = args.short
    __builtin__.long = args.long
    if args.output:
        output = args.output.split(',')
        __builtin__.output = output
    else:
        __builtin__.output = prefered_output
    search = args.search
    public = args.public
    nocache = args.nocache
    oroperand = args.oroperand
    version = args.version
    if args.testnstuff:
        test()
    if version:
        show_version()
        sys.exit(0)
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    if nocache:
        expire_cache()
    if args.listall:
        instances = aws_inventory(create_index=True)
        display_results_ordered(instances)
    elif search:
        print "Searching for %s" % search
        results = searchfor(search, oroperand)
        if connect:
            connect_to(results)
    elif public:
        pub_ip()
    else:
        instances = aws_inventory(create_index=True)
        display_results_ordered(instances)

def show_version():
    print "Loony version %s " % __version__


if __name__ == '__main__':
    main()