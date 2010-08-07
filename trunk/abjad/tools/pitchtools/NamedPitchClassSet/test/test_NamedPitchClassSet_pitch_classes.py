from abjad import *


def test_NamedPitchClassSet_pitch_classes_01( ):

   npc_set = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),])
   pitch_classes = npc_set.pitch_classes

   assert isinstance(pitch_classes, tuple)

   assert pitch_classes[0] == pitchtools.NumericPitchClass(0)
   assert pitch_classes[1] == pitchtools.NumericPitchClass(2)
   assert pitch_classes[2] == pitchtools.NumericPitchClass(4)
