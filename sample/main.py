#!/usr/bin/env python

import argparse
import logging

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='Increase log verbosity')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='Debug level verbosity')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    main()