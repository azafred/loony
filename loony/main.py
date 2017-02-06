#!/usr/bin/env python

import argparse
import logging
from aws_fetcher import aws_inventory
from display import display_results_ordered


def main():

    parser = argparse.ArgumentParser()
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
        '-stp', '--stopped', action='store_true', default=False,
        help='Include stopped instances as well', dest='stopped')

    args = parser.parse_args()
    stopped = args.stopped
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    if args.listall:
        instances = aws_inventory()
        display_results_ordered(instances, stopped)


if __name__ == '__main__':
    main()