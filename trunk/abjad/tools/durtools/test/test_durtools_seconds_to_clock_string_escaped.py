from abjad import *
import py.test


def test_durtools_seconds_to_clock_string_escaped_01( ):
   
   assert durtools.seconds_to_clock_string_escaped(0) == "0'00\\\""
   assert durtools.seconds_to_clock_string_escaped(4) == "0'04\\\""
   assert durtools.seconds_to_clock_string_escaped(20) == "0'20\\\""
   assert durtools.seconds_to_clock_string_escaped(60) == "1'00\\\""
   assert durtools.seconds_to_clock_string_escaped(120) == "2'00\\\""
   assert durtools.seconds_to_clock_string_escaped(240) == "4'00\\\""
