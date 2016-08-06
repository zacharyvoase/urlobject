#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='URLObject',
    version='2.4.2',
    description='A utility class for manipulating URLs.',
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/zacharyvoase/urlobject',
    packages=find_packages(exclude=('test',)),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
