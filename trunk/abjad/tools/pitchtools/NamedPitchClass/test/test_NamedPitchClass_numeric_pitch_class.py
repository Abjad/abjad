from abjad import *


def test_NamedPitchClass_numbered_chromatic_pitch_class_01( ):

   npc = pitchtools.NamedPitchClass('c')
   assert npc.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(0)

   npc = pitchtools.NamedPitchClass('cs')
   assert npc.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)

   npc = pitchtools.NamedPitchClass('cf')
   assert npc.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(11)

   npc = pitchtools.NamedPitchClass('cqs')
   assert npc.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(0.5)
