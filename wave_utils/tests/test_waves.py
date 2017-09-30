#!usr/bin/env python

"""
some simple tests --  not at all complete
"""

# py2/3 compatible:
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pytest

from wave_utils import waves


def test_import():
    """ is there anything there? """
    assert hasattr(waves, 'wave_number')

def test_frequency():
    """
    Test the wave frequency

    The test is done for multiple values and most importantly edge cases, due to
    the sqrt in the equation.
    """
    assert abs(4.59043034 - waves.frequency(waves.g, 3.0, 0.3)) < 1e-7
    assert abs(0.0 - waves.frequency(waves.g, 0.0, 0.3)) < 1e-7
    assert abs(4.59043034 - waves.frequency(waves.g, -3.0, 0.3)) < 1e-7

    assert np.isnan(waves.frequency(waves.g, -3.0, 0.3)) == 0

def test_celerity_deep():
    h = 10000 # very deep
    omega = 2*np.pi/1 # short period wave
    k = waves.wave_number(waves.g, omega, h)   # short waves
    C = waves.celerity(k, h, waves.g)
    assert C == waves.g / omega # should be for deep water -- in this case exact!

def test_celerity_shallow():
    h = 1 # shallow
    k = 2*np.pi/10000 # long waves
    C = waves.celerity(k, h, waves.g)
    assert np.allclose(C, np.sqrt(waves.g * h), rtol=1e-7) # should be for shallow
