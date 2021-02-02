#!/usr/bin/env python

from setuptools import setup

__version__ = "0.5.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='json-coder',
      version=__version__,
      description='Easily deserialize and serialize complex objects to json.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Max Zhao',
      author_email='alcasa.mz@gmail.com',
      url='https://github.com/xiamaz/jsonify',
      packages=['json_coder'],
      python_requires='>=3.6',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
     )
