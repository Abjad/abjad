from abjad import *
from abjad.tools import durationtools


def test_durationtools_lilypond_duration_string_to_rational_list_01():

    duration_string = '8.. 32 8.. 32'
    rationals = durationtools.lilypond_duration_string_to_rational_list(duration_string)

    assert rationals == [
        Fraction(7, 32), Fraction(1, 32), Fraction(7, 32), Fraction(1, 32)]
