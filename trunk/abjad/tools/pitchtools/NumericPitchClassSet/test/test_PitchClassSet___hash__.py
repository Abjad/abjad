from abjad import *


def test_PitchClassSet___hash___01( ):
   '''Pitch class sets are hashable.'''

   pcset = pitchtools.NumericPitchClassSet([0, 1, 2])

   assert hash(pcset) == hash(repr(pcset))
