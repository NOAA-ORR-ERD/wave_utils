#!/usr/bin/env python

"""
setup.py for wave_utils
"""
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


# to make "setup.py test" work
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.verbose = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def get_version():
    """
    return the version number from the __init__
    """
    for line in open("wave_utils/__init__.py"):
        if line.startswith("__version__"):
            version = line.strip().split('=')[1].strip().strip("'").strip('"')
            return version
    raise ValueError("can't find version string in __init__")


setup(
    name="wave_utils",
    version=get_version(),
    description="Utilities for computing properties of ocean waves",
    long_description=open('README.rst').read(),
    author="Chris Barker",
    author_email="chris.barker@noaa.gov",
    url="https://github.com/ChrisBarker-NOAA/wave_utils",
    download_url="https://github.com/ChrisBarker-NOAA/wave_utils/archive/v0.1.1.tar.gz",
    license="Public Domain",
    # keywords = "",
    packages=["wave_utils"],
    tests_require=['pytest'],
    cmdclass=dict(test=PyTest),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering",
    ],
)
