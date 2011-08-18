from abjad import *
from abjad.tools import mathtools


def test_mathtools_integer_equivalent_number_to_integer_01():
    '''Change integer-equivalent number to integer.
    '''

    assert mathtools.integer_equivalent_number_to_integer(17.0) == 17


def test_mathtools_integer_equivalent_number_to_integer_02():
    '''Return noninteger-equivalent number unchanged.
    '''

    assert mathtools.integer_equivalent_number_to_integer(17.5) == 17.5
