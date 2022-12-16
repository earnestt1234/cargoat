#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup for cargoat.

@author: Tom Earnest
"""

from os import path

from setuptools import setup

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# read version
with open(path.join(this_directory, 'cargoat', '_version.py'), encoding='utf-8') as f:
    version = f.read().split('=')[1].strip('\'"')

setup(name='cargoat',
      version=version,
      python_requires='>=3.8',
      description='Custom Monty Hall problem simulations in Python.',
      url='https://github.com/earnestt1234/cargoat',
      author='Tom Earnest',
      author_email='earnestt1234@gmail.com',
      license='MIT',
      packages=['cargoat'],
      install_requires=['numpy>=1.2'],
      long_description=long_description,
      long_description_content_type='text/markdown')
