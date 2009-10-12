from abjad import *


def test_pitchtools_PitchClass___add___01( ):

   pc1 = pitchtools.PitchClass(6)
   pc2 = pitchtools.PitchClass(7)

   assert pc1 + pc2 == pitchtools.PitchClass(1)
