from abjad import *


def test_NumericPitchClassSet___contains___01( ):
   '''PitchClassSet containment works as expected.'''

   pcset = pitchtools.NumericPitchClassSet([0, 2, 6, 7])
   pc1 = pitchtools.NumericPitchClass(2)
   pc2 = pitchtools.NumericPitchClass(3)
   
   assert pc1 in pcset
   assert pc2 not in pcset
