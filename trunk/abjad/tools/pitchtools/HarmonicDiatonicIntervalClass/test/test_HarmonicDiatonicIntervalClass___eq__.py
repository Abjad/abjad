from abjad import *


def test_HarmonicDiatonicIntervalClass___eq__01( ):

   hdic_1 = pitchtools.HarmonicDiatonicIntervalClass('perfect', 1)
   hdic_2 = pitchtools.HarmonicDiatonicIntervalClass('perfect', -1)

   assert hdic_1 == hdic_2
   assert hdic_2 == hdic_1

   assert not hdic_1 != hdic_2
   assert not hdic_2 != hdic_1

   assert not hdic_1 is hdic_2
   assert not hdic_2 is hdic_1
