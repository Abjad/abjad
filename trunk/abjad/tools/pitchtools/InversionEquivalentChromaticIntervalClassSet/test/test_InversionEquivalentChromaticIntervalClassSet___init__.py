from abjad import *


def test_InversionEquivalentChromaticIntervalClassSet___init___01( ):

   ics = pitchtools.InversionEquivalentChromaticIntervalClassSet([1, 5, 1, 1, 3])
   assert ics.numbers == set([1, 3, 5])
