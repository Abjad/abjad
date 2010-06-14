from abjad import *


def test_tonalharmony_is_passing_tone_01( ):

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   
   assert not tonalharmony.is_passing_tone(t[0])
   assert tonalharmony.is_passing_tone(t[1])
   assert tonalharmony.is_passing_tone(t[2])
   assert not tonalharmony.is_passing_tone(t[3])
