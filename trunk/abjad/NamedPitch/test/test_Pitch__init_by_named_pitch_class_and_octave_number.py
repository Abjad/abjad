from abjad import *


def test_Pitch__init_by_named_pitch_class_and_octave_number_01( ):

   npc = pitchtools.NamedPitchClass('cs')
   octave_number = 5
   pitch = Pitch(npc, octave_number)

   assert pitch == Pitch('cs', 5)
