#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import os
import subprocess
from setuptools import setup, find_packages
from codecs import open
# from loony import version as loonyver
#import versioneer
import sys

# print(loonyver.__version__)

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

with open('LICENSE', encoding='utf-8') as f:
    license = f.read()

# Fetching version from git tag...
try:
    version_git = subprocess.check_output(["git", "describe", "--tags"]).rstrip()
    print("Version from git: {}".format(version_git))
except:
    version_git = 'x.x.x'
    print("Version: {}".format(version_git))


setup(
    name='loony',
    #version=versioneer.get_version(),
    #cmdclass=versioneer.get_cmdclass(),
    version=version_git,
    description='Script to search and connect to EC2 instances.',
    long_description=readme,
    author='Fred Vassard',
    author_email='fred@studyblue.com',
    url='http://loony.studyblue.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['libtmux','boto','colorama','prettytable','decorator','pyyaml', 'quik', 'decorating', 'animation', 'wget', 'tqdm', 'requests'],
    setup_requires=['libtmux','boto','colorama','prettytable','decorator','pyyaml', 'quik', 'decorating', 'animation', 'wget', 'tqdm', 'requests'],
    tests_require=['nose', 'testfixtures', 'mock'],
    test_suite="nose.collector",
    entry_points={
        'console_scripts': [
            'loony = loony.main:main',
            'connect = loony.main:connect',
        ],
    },
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
)

