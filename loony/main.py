#!/usr/bin/env python


import argparse
import logging
import sys, os
import shlex
import requests
import os
import wget
import config
from subprocess import check_call, call, check_output
from aws_fetcher import aws_inventory, list_keys
from display import display_results_ordered
from search import searchfor
from connect import connect_to
from cache import expire_cache
from settings import *
from _version import get_versions
from version import __version__
from tqdm import tqdm

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


def check_current():
    url = "https://s3.amazonaws.com/studyblue-binaries/latest_version.txt"
    r = requests.get(url)
    latest = r.content.rstrip()
    if latest == __version__:
        #current
        return True
    else:
        print("Current version: {}".format(__version__))
        print("latest version: {}".format(latest))
        return False


def upgrade_loony():
    print("Upgrading Loony. Please wait...")
    cur_file = os.path.realpath(__file__)
    print("Cu")
    cmd = shlex.split('file {}'.format(cur_file))
    filetype = check_output(cmd)
    if 'site-packages' in cur_file:
        print("\tIt looks like you are using the python source. Upgrading via pip.")
        try:
            cmd = "sudo -H pip install --upgrade loony"
            parsed_cmd = shlex.split(cmd)
            exit_code = check_call(parsed_cmd)
            print(exit_code)
        except Exception as e:
            print("Problem with pip: {}".format(str(e)))
    else:
        print("\tIt looks like you are running the binary version of loony.")
        os_version = os.uname()[0]
        if 'Darwin' in os_version:
            url = "https://s3.amazonaws.com/studyblue-binaries/loony_macos_latest"
        else:
            url = "https://s3.amazonaws.com/studyblue-binaries/loony_linux_latest"
        print("Downloading latest version from {}".format(url))
        try:
            wget.download(url, out='/usr/local/bin/loony')
            os.chmod('/usr/local/bin/loony', 755)
        except Exception as e:
            print("Problem with wget: {}".format(str(e)))


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
        help='Display long-format results', dest='long_format')
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
        '-p', '--public', action='store_true',
        default=False,
        help="Connect via public IP instead.",
        dest='public_ip')
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
    config.short = args.short
    config.verbose = args.verbose
    config.debug = args.debug
    config.long_format = args.long_format
    if args.output:
        config.output = args.output.split(',')
    else:
        config.output = prefered_output
    search = args.search
    if 'devstack' in search:
        config.devstack_format = True
    else:
        config.devstack_format = False
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
    public_ip = args.public_ip
    if upgrade:
        upgrade_loony()
        sys.exit(0)
    elif not check_current():
        print("It looks like you are not running the latest version of loony. Upgrade with loony --upgrade.")
        # upgrade_loony()
        # sys.exit(0)
    if version:
        show_version()
        sys.exit(0)
    if not check_aws_creds():
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
        if orsearch:
            print( "Searching for {} or {}").format(search, orsearch)
            results = searchfor(search, orsearch, notable=notable)
        else:
            print( "Searching for %s" )% search
            results = searchfor(search, notable=notable)
        if connect or connectcli or cmd:
            if user:
                connect_to(results, public=public_ip, user=user, cmd=cmd, batch=batchmode, one_only=one_only)
            else:
                connect_to(results, public=public_ip, cmd=cmd, batch=batchmode, one_only=one_only)

    else:
        instances = aws_inventory()
        display_results_ordered(instances, notable=notable)

def show_version():
    # __version__ = get_versions()['version']
    print( "Loony version %s ") % __version__


if __name__ == '__main__':
    main()
