from abjad import *
from abjad.tools import seqtools


def test_seqtools_all_are_positive_integer_equivalent_numbers_01( ):

    assert seqtools.all_are_positive_integer_equivalent_numbers([Fraction(4, 2), 2.0, 2])


def test_seqtools_all_are_positive_integer_equivalent_numbers_02( ):

    assert not seqtools.all_are_positive_integer_equivalent_numbers([Fraction(5, 2), 2.5, -2, 0])
