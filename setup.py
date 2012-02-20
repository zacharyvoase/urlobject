#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distribute_setup import use_setuptools; use_setuptools()
from setuptools import setup, find_packages


setup(
    name='URLObject',
    version='2.0.0',
    description='A utility class for manipulating URLs.',
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/zacharyvoase/urlobject',
    package_dir={'': 'lib'},
    packages=find_packages(where='lib'),
)
