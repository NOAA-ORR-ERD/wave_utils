#!usr/bin/env python

"""
some simple tests --  not at all complete
"""

# py2/3 compatible:
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from wave_utils import waves 

#some constants:
g = 9.806
pi = np.pi

def test_import():
    """ is there anything there? """
    assert hasattr(waves, 'wave_number')

def test_celerity_deep():
    h = 10000 # very deep
    omega = 2*pi/1 # short period wave
    k = waves.wave_number(g, omega, h)   # short waves
    C = waves.celerity(k, h, g)
    assert C == g / omega # should be for deep water -- in this case exact!
    
def test_celerity_shallow():
    h = 1 # shallow
    k = 2*pi/10000 # long waves
    C = waves.celerity(k, h, g)
    assert np.allclose(C, np.sqrt(g * h), rtol=1e-7) # should be for shallow


