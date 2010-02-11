from abjad import *


def test_PitchClassSet_pitch_classes_01( ):

   npc_set = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),])
   pitch_classes = npc_set.pitch_classes

   assert isinstance(pitch_classes, tuple)

   assert pitch_classes[0] == pitchtools.PitchClass(0)
   assert pitch_classes[1] == pitchtools.PitchClass(2)
   assert pitch_classes[2] == pitchtools.PitchClass(4)
