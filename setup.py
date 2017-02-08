# -*- coding: utf-8 -*-
import os
import subprocess
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

# Fetching version from git tag...
version_py = os.path.join(os.path.dirname(__file__), 'version.py')
try:
    version_git = subprocess.check_output(["git", "describe"]).rstrip()
except:
    with open(version_py, 'r') as fh:
        version_git = open(version_py).read().strip().split('=')[-1].replace('"','')

version_msg = "# Do not edit this file, pipeline versioning is governed by git tags"
with open(version_py, 'w') as fh:
    fh.write(version_msg + os.linesep + "__version__=" + version_git)


setup(
    name='loony',
    version="{ver}".format(ver=version_git),
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Fred Vassard',
    author_email='azafred@gmail.com',
    url='https://github.com/azafred/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['boto','colorama','prettytable','decorator','pyyaml', 'quik', 'pyobjc-framework-Cocoa'],
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

