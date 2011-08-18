from abjad import *
from abjad.tools import mathtools


def test_mathtools_binomial_coefficient_01():

    assert mathtools.binomial_coefficient(8, 0) == 1
    assert mathtools.binomial_coefficient(8, 1) == 8
    assert mathtools.binomial_coefficient(8, 2) == 28
    assert mathtools.binomial_coefficient(8, 3) == 56
    assert mathtools.binomial_coefficient(8, 4) == 70
    assert mathtools.binomial_coefficient(8, 5) == 56
    assert mathtools.binomial_coefficient(8, 6) == 28
    assert mathtools.binomial_coefficient(8, 7) == 8
    assert mathtools.binomial_coefficient(8, 8) == 1
