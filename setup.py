# -*- coding: utf-8 -*-
import os
import subprocess
from setuptools import setup, find_packages
import versioneer



with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

# Fetching version from git tag...
try:
    version_git = subprocess.check_output(["git", "describe", "--tags"]).rstrip()
except:
    version_git = 'x.x.x'


setup(
    name='loony',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Fred Vassard',
    author_email='azafred@gmail.com',
    url='https://github.com/azafred/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['libtmux','boto','colorama','prettytable','decorator','pyyaml', 'quik', 'pyobjc-framework-Cocoa'],
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
        'Operating System :: MacOS',
      ],
)

