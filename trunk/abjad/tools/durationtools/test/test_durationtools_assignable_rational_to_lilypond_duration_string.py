from abjad import *
from abjad.tools import durationtools
import py.test


def test_durationtools_assignable_rational_to_lilypond_duration_string_01():

    assert durationtools.assignable_rational_to_lilypond_duration_string(Fraction(1, 16)) == '16'
    assert durationtools.assignable_rational_to_lilypond_duration_string(Fraction(2, 16)) == '8'
    assert durationtools.assignable_rational_to_lilypond_duration_string(Fraction(3, 16)) == '8.'
    assert durationtools.assignable_rational_to_lilypond_duration_string(Fraction(4, 16)) == '4'


def test_durationtools_assignable_rational_to_lilypond_duration_string_02():

    assert py.test.raises(AssignabilityError,
        'durationtools.assignable_rational_to_lilypond_duration_string(Fraction(5, 16))')
