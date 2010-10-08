from abjad import *


def test_NamedPitchClassSet_pitch_classes_01( ):

   npc_set = pitchtools.NamedChromaticPitchClassSet([
      pitchtools.NamedChromaticPitchClass('c'),
      pitchtools.NamedChromaticPitchClass('d'),
      pitchtools.NamedChromaticPitchClass('e'),])
   pitch_classes = npc_set.pitch_classes

   assert isinstance(pitch_classes, tuple)

   assert pitch_classes[0] == pitchtools.NumberedChromaticPitchClass(0)
   assert pitch_classes[1] == pitchtools.NumberedChromaticPitchClass(2)
   assert pitch_classes[2] == pitchtools.NumberedChromaticPitchClass(4)
