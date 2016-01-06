#!/usr/bin/env python

"""
setup.py for wave_utils
"""
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
## to make "setup.py test" work

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.verbose = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

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
    tests_require=['pytest'],
    cmdclass=dict(test=PyTest),
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

