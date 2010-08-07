from abjad import *


def test_NamedPitchClass_numeric_pitch_class_01( ):

   npc = pitchtools.NamedPitchClass('c')
   assert npc.numeric_pitch_class == pitchtools.NumericPitchClass(0)

   npc = pitchtools.NamedPitchClass('cs')
   assert npc.numeric_pitch_class == pitchtools.NumericPitchClass(1)

   npc = pitchtools.NamedPitchClass('cf')
   assert npc.numeric_pitch_class == pitchtools.NumericPitchClass(11)

   npc = pitchtools.NamedPitchClass('cqs')
   assert npc.numeric_pitch_class == pitchtools.NumericPitchClass(0.5)
