#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='jsonify',
      version='0.1',
      description='Easily desrialize and serialize complex objects to json.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Max Zhao',
      author_email='alcasa.mz@gmail.com',
      url='https://github.com/xiamaz/jsonify',
      packages=['jsonify'],
      python_requires='>=3.6',
     )
