from abjad import *


def test_NumericPitchClassSet_pitch_classes_01( ):

   pcset = pitchtools.NumericPitchClassSet([0, 6, 10, 4, 9, 2])
   pitch_classes = pcset.pitch_classes

   assert isinstance(pitch_classes, tuple)

   assert pitch_classes[0].number == 0
   assert pitch_classes[1].number == 2
   assert pitch_classes[2].number == 4
   assert pitch_classes[3].number == 6
   assert pitch_classes[4].number == 9
   assert pitch_classes[5].number == 10
