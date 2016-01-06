#!/usr/bin/env python

"""
setup.py for wave_utils
"""

from setuptools import setup

setup(
    name="wave_utils",
    version='0.1.0',
    description="Utilities for computing properties of ocean waves",
    long_description=open('README.md').read(),
    author="Chris Barker",
    author_email="chris.barker@noaa.gov",
    url="https://github.com/ChrisBarker-NOAA",
    license="Public Domain",
    # keywords = "",
    packages=["wave_utils"],
#    tests_require=['pytest'],
#    cmdclass=dict(test=PyTest),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: Public Domain",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering",
    ],
)

