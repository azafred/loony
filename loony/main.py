#!/usr/bin/env python


import argparse
import logging
import __builtin__
import sys, os
import shlex
from subprocess import check_call, call
from aws_fetcher import aws_inventory, list_keys
from display import display_results_ordered
from search import searchfor
from connect import connect_to
from cache import expire_cache
from settings import *
from _version import get_versions
from version import __version__

import os
if not os.getenv('PYTHONIOENCODING', None): # PyInstaller workaround
    os.environ['PYTHONIOENCODING'] = 'utf_8'


def check_aws_creds():
    creds_ok = False
    try:
        with open(os.path.expanduser('~/.aws/credentials'), 'r') as fh:
            for lines in fh.readlines():
                if 'aws_access_key_id' in lines:
                    creds_ok = True
    except Exception as e:
        print(e)
        print("It appears your AWS credentials are not setup.\nPlease edit ~/.aws/credentials with your keys:\n")
        print("""
        [default]
        region = us-east-1
        aws_access_key_id = XXXXXXXXX
        aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXX
        output = text

        [dev]
        region = us-east-1
        aws_access_key_id = XXXXXXXXX
        aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXX
        output = text
        """)
    return creds_ok


def upgrade_loony():
    cmd = "sudo -H pip install --upgrade git+ssh://git@github.com/StudyBlue/loony.git"
    parsed_cmd = shlex.split(cmd)
    exit_code = check_call(parsed_cmd)
    print(exit_code)


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
        '-nc', '--nocache', action='store_true', default=False,
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
        '-b', '--batch', action='store_true',
        default=False,
        help="Batch mode. Won't use tmux to run cmd",
        dest='batchmode')
    parser.add_argument(
        '-nt', '--notable', action='store_true',
        default=False,
        help="Don't print an ascii table",
        dest='notable')
    parser.add_argument(
        '-1', action='store_true',
        default=False,
        help='connect to only one of the result instances (choice)',
        dest='one_only')
    parser.add_argument(
        '--cmd', type=str, nargs='?',
        help='Run this command on resulting hosts', dest='cmd')
    parser.add_argument(
        '-or', "--or", metavar='orsearch', type=str, nargs='*',
        help='things to or in a search', dest='orsearch')
    parser.add_argument(
        '--upgrade', action='store_true', default=False,
        help='upgrade Loony',
        dest='upgrade')
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
    orsearch = args.orsearch
    nocache = args.nocache
    version = args.version
    listkeys = args.listkeys
    connectcli = args.connectcli
    batchmode = args.batchmode
    one_only = args.one_only
    notable = args.notable
    cmd = args.cmd
    user = args.user
    upgrade = args.upgrade
    if upgrade:
        upgrade_loony()
        sys.exit(0)
    if version:
        show_version()
        sys.exit(0)
    if not check_aws_creds():
        sys.exit(1)
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    if nocache:
        expire_cache()
    if listkeys:
        list_keys()
    elif search:
        if orsearch:
            print( "Searching for {} or {}").format(search, orsearch)
            results = searchfor(search, orsearch, notable=notable)
        else:
            print( "Searching for %s" )% search
            results = searchfor(search, notable=notable)
        if connect or connectcli or cmd:
            if user:
                connect_to(results, user=user, cmd=cmd, batch=batchmode, one_only=one_only)
            else:
                connect_to(results, cmd=cmd, batch=batchmode, one_only=one_only)

    else:
        instances = aws_inventory()
        display_results_ordered(instances, notable=notable)

def show_version():
    # __version__ = get_versions()['version']
    print( "Loony version %s ") % __version__


if __name__ == '__main__':
    main()
