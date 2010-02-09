from abjad import *


def test_NamedPitchClass_pitch_class_01( ):

   npc = tonalharmony.NamedPitchClass('c')
   assert npc.pitch_class == pitchtools.PitchClass(0)

   npc = tonalharmony.NamedPitchClass('cs')
   assert npc.pitch_class == pitchtools.PitchClass(1)

   npc = tonalharmony.NamedPitchClass('cf')
   assert npc.pitch_class == pitchtools.PitchClass(11)

   npc = tonalharmony.NamedPitchClass('cqs')
   assert npc.pitch_class == pitchtools.PitchClass(0.5)
