from abjad import *
from abjad.tools import durationtools


def test_durationtools_lilypond_duration_string_to_rational_01():

    assert durationtools.lilypond_duration_string_to_rational('8') == Fraction(1, 8)
    assert durationtools.lilypond_duration_string_to_rational('8.') == Fraction(3, 16)
    assert durationtools.lilypond_duration_string_to_rational('8..') == Fraction(7, 32)
    assert durationtools.lilypond_duration_string_to_rational('8...') == Fraction(15, 64)


def test_durationtools_lilypond_duration_string_to_rational_02():

    assert durationtools.lilypond_duration_string_to_rational(r'\breve') == Fraction(2, 1)
    assert durationtools.lilypond_duration_string_to_rational(r'\breve.') == Fraction(3, 1)
    assert durationtools.lilypond_duration_string_to_rational(r'\breve..') == Fraction(7, 2)
    assert durationtools.lilypond_duration_string_to_rational(r'\breve...') == Fraction(15, 4)
