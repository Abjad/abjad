from abjad import *
from abjad.tools import durationtools
import py.test


def test_durationtools_numeric_seconds_to_clock_string_01():

    assert durationtools.numeric_seconds_to_clock_string(0) == "0'00\""
    assert durationtools.numeric_seconds_to_clock_string(4) == "0'04\""
    assert durationtools.numeric_seconds_to_clock_string(20) == "0'20\""
    assert durationtools.numeric_seconds_to_clock_string(60) == "1'00\""
    assert durationtools.numeric_seconds_to_clock_string(120) == "2'00\""
    assert durationtools.numeric_seconds_to_clock_string(240) == "4'00\""


def test_durationtools_numeric_seconds_to_clock_string_02():

    assert durationtools.numeric_seconds_to_clock_string(Fraction(0)) == "0'00\""
    assert durationtools.numeric_seconds_to_clock_string(Fraction(3, 2)) == "0'01\""
    assert durationtools.numeric_seconds_to_clock_string(Fraction(89, 14)) == "0'06\""
    assert durationtools.numeric_seconds_to_clock_string(Fraction(116, 19)) == "0'06\""
    assert durationtools.numeric_seconds_to_clock_string(Fraction(140, 3)) == "0'46\""
    assert durationtools.numeric_seconds_to_clock_string(Fraction(180, 3)) == "1'00\""


def test_durationtools_numeric_seconds_to_clock_string_03():

    assert py.test.raises(ValueError, 'durationtools.numeric_seconds_to_clock_string(-1.5)')
