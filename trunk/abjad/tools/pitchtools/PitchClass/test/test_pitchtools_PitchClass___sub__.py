from abjad import *


def test_pitchtools_PitchClass___sub___01( ):

   pc1 = pitchtools.PitchClass(6)
   pc2 = pitchtools.PitchClass(7)

   #assert pc1 - pc2 == pitchtools.PitchClass(11)
   #assert pc2 - pc1 == pitchtools.PitchClass(1)

   assert pc1 - pc2 == pitchtools.IntervalClass(1)
   assert pc2 - pc1 == pitchtools.IntervalClass(1)
