from abjad import *


def test_NumberedChromaticPitchClassSet_pitch_classes_01( ):

   pcset = pitchtools.NumberedChromaticPitchClassSet([0, 6, 10, 4, 9, 2])
   pitch_classes = pcset.pitch_classes

   assert isinstance(pitch_classes, tuple)

   assert pitch_classes[0] == 0
   assert pitch_classes[1] == 2
   assert pitch_classes[2] == 4
   assert pitch_classes[3] == 6
   assert pitch_classes[4] == 9
   assert pitch_classes[5] == 10
