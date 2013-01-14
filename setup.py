#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='URLObject',
    version='2.2.0',
    description='A utility class for manipulating URLs.',
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/zacharyvoase/urlobject',
    packages=find_packages(exclude=('test',)),
)
