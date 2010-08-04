from abjad import *


def test_NamedPitch__init_by_named_pitch_class_and_octave_number_01( ):

   npc = pitchtools.NamedPitchClass('cs')
   octave_number = 5
   pitch = NamedPitch(npc, octave_number)

   assert pitch == NamedPitch('cs', 5)
