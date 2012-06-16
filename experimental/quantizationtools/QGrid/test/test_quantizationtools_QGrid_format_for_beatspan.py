from fractions import Fraction
from experimental.quantizationtools import QGrid


def test_quantizationtools_QGrid_format_for_beatspan_01():

    assert QGrid([0], 0).format_for_beatspan().lilypond_format == \
        "{\n\tc'4\n}"
    assert QGrid([0], 0).format_for_beatspan(Fraction(1, 4)).lilypond_format == \
        "{\n\tc'4\n}"
    assert QGrid([0], 0).format_for_beatspan(Fraction(1, 8)).lilypond_format == \
        "{\n\tc'8\n}"
    assert QGrid([0, 0, 0], 0).format_for_beatspan(Fraction(1, 4)).lilypond_format == \
        "\\times 2/3 {\n\tc'8\n\tc'8\n\tc'8\n}"
    assert QGrid([0, [0, [0, 0], 0], 0, 0, 0], 0).format_for_beatspan(Fraction(1, 2)).lilypond_format == \
        "\\times 4/5 {\n\tc'8\n\t\\times 2/3 {\n\t\tc'16\n\t\tc'32\n\t\tc'32\n\t\tc'16\n\t}\n\tc'8\n\tc'8\n\tc'8\n}"
    assert QGrid([0, [0, [0, [0, 0]]]], 0).format_for_beatspan().lilypond_format == \
        "{\n\tc'8\n\tc'16\n\tc'32\n\tc'64\n\tc'64\n}"
