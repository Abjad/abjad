from abjad import *
from abjad.tools import durationtools
import py.test


def test_durationtools_numeric_seconds_to_escaped_clock_string_01():

    assert durationtools.numeric_seconds_to_escaped_clock_string(0) == "0'00\\\""
    assert durationtools.numeric_seconds_to_escaped_clock_string(4) == "0'04\\\""
    assert durationtools.numeric_seconds_to_escaped_clock_string(20) == "0'20\\\""
    assert durationtools.numeric_seconds_to_escaped_clock_string(60) == "1'00\\\""
    assert durationtools.numeric_seconds_to_escaped_clock_string(120) == "2'00\\\""
    assert durationtools.numeric_seconds_to_escaped_clock_string(240) == "4'00\\\""
