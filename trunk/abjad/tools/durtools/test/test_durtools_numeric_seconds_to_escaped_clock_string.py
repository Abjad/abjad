from abjad import *
from abjad.tools import durtools
import py.test


def test_durtools_numeric_seconds_to_escaped_clock_string_01():

    assert durtools.numeric_seconds_to_escaped_clock_string(0) == "0'00\\\""
    assert durtools.numeric_seconds_to_escaped_clock_string(4) == "0'04\\\""
    assert durtools.numeric_seconds_to_escaped_clock_string(20) == "0'20\\\""
    assert durtools.numeric_seconds_to_escaped_clock_string(60) == "1'00\\\""
    assert durtools.numeric_seconds_to_escaped_clock_string(120) == "2'00\\\""
    assert durtools.numeric_seconds_to_escaped_clock_string(240) == "4'00\\\""

