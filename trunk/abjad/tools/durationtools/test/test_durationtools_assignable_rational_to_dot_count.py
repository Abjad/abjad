from abjad import *
from abjad.tools import durationtools
import py.test


def test_durationtools_assignable_rational_to_dot_count_01():

    assert durationtools.assignable_rational_to_dot_count(Fraction(1, 16)) == 0
    assert durationtools.assignable_rational_to_dot_count(Fraction(2, 16)) == 0
    assert durationtools.assignable_rational_to_dot_count(Fraction(3, 16)) == 1
    assert durationtools.assignable_rational_to_dot_count(Fraction(4, 16)) == 0

    assert durationtools.assignable_rational_to_dot_count(Fraction(6, 16)) == 1
    assert durationtools.assignable_rational_to_dot_count(Fraction(7, 16)) == 2
    assert durationtools.assignable_rational_to_dot_count(Fraction(8, 16)) == 0


def test_durationtools_assignable_rational_to_dot_count_02():

    assert py.test.raises(AssignabilityError,
        'durationtools.assignable_rational_to_dot_count(Fraction(5, 16))')
