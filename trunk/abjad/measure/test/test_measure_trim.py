from abjad import *


def test_measure_trim_01( ):
   '''Nonnegative indices work.'''
   t = Measure((4, 8), Note(0, (1, 8)) * 4)
   t.trim(0)
   assert t.format == "\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8"
   assert check(t)


def test_measure_trim_02( ):
   '''Negative indices work.'''
   t = Measure((4, 8), Note(0, (1, 8)) * 4)
   t.trim(-1)
   assert t.format == "\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8"
   assert check(t)
   

def test_measure_trim_03( ):
   '''Denominator preservation in meter.'''
   t = Measure((4, 8), Note(0, (1, 8)) * 4)
   t.trim(0, 2)
   assert t.format == "\t\\time 2/8\n\tc'8\n\tc'8"
   assert check(t)


def test_measure_trim_04( ):
   '''Denominator changes from 8 to 16.'''
   t = Measure((4, 8), Note(0, (1, 16)) * 2 + Note(0, (1, 8)) * 3)
   t.trim(0)
   assert t.format == "\t\\time 7/16\n\tc'16\n\tc'8\n\tc'8\n\tc'8"
   assert check(t)
