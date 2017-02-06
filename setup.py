# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Fred Vassard',
    author_email='azafred@gmail.com',
    url='https://github.com/azafred/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['pyyaml', 'quik', 'pyobjc-framework-Cocoa'],
    tests_require=['nose', 'testfixtures', 'mock'],
    test_suite="nose.collector",
    entry_points={
        'console_scripts': [
          'sample = sample.main:main',
        ],
      },
      classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Operating System :: MacOS',
      ],
     )
)

