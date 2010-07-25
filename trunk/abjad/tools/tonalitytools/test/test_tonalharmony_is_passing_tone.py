from abjad import *


def test_tonalitytools_is_passing_tone_01( ):

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   
   assert not tonalitytools.is_passing_tone(t[0])
   assert tonalitytools.is_passing_tone(t[1])
   assert tonalitytools.is_passing_tone(t[2])
   assert not tonalitytools.is_passing_tone(t[3])
