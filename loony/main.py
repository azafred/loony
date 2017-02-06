#!/usr/bin/env python

import argparse
import logging
from aws_fetcher import aws_inventory
from display import display_results_ordered
from search import searchfor


def main():

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
        'search', metavar='search', type=str, nargs='+',
        help='Search parameters')

    args = parser.parse_args()
    stopped = args.stopped
    running = args.running
    search = args.search
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    if args.listall:
        instances = aws_inventory()
        display_results_ordered(instances, stopped, running)
    if search:
        print "Searching for %s" % search
        searchfor(search)

if __name__ == '__main__':
    main()