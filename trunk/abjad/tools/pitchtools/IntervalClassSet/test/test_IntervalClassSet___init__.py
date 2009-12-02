from abjad import *


def test_IntervalClassSet___init___01( ):

   ics = pitchtools.IntervalClassSet([1, 5, 1, 1, 3])
   assert ics.numbers == set([1, 3, 5])
