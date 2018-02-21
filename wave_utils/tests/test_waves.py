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


@pytest.mark.parametrize(("k", "h", "exp_omega"), [(3.0, 0.3, 4.59058248),
                                                   (0.0, 0.3, 0.0),
                                                   (-3.0, 0.3, 4.59058248),
                                                   ])
def test_frequency(k, h, exp_omega):
    """
    Test the wave frequency

    The test is done for multiple values and most importantly edge cases, due to
    the sqrt in the equation.

    signature: frequency(g, k, h)
    """
    assert np.isclose(exp_omega, waves.frequency(waves.g, k, h), atol=1e-7)


def test_dispersion():
    """ one arbitrary value """
    assert np.isclose(1.199678640, waves.dispersion(1.0), atol=1e-7)


def test_dispersion_zero_depth():
    with pytest.raises(ValueError):
        waves.dispersion(0.0)


def test_celerity_deep():
    h = 10000  # very deep
    omega = 2 * np.pi / 1.0  # short period wave
    k = waves.wave_number(waves.g, omega, h)   # short waves
    C = waves.celerity(k, h, waves.g)
    # should be for deep water
    assert np.isclose(C, waves.g / omega, rtol=1e-15, atol=0.0)


def test_celerity_inf():
    # does it work with infinate depth?
    h = np.inf
    omega = 2 * np.pi / 100.0  # long-ish wave (but still short for inf deep!)
    k = waves.wave_number(waves.g, omega, h)   # short waves
    C = waves.celerity(k, h, waves.g)
    # should be for deep water
    assert np.isclose(C, waves.g / omega, rtol=1e-15, atol=0.0)


def test_celerity_shallow():
    h = 1.0  # shallow
    k = 2 * np.pi / 10000  # long waves
    C = waves.celerity(k, h, waves.g)
    assert np.allclose(C, np.sqrt(waves.g * h), rtol=1e-7)  # should be for shallow
