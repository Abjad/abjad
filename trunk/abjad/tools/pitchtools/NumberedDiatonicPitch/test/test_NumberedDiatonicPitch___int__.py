from abjad import *


def test_NumberedDiatonicPitch___int___01( ):

   assert pitchtools.NumberedDiatonicPitch(-1) == -1
   assert pitchtools.NumberedDiatonicPitch(0) == 0
   assert pitchtools.NumberedDiatonicPitch(6) == 6
   assert pitchtools.NumberedDiatonicPitch(7) == 7
   assert pitchtools.NumberedDiatonicPitch(13) == 13
   assert pitchtools.NumberedDiatonicPitch(14) == 14
