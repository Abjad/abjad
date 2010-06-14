from abjad import *


def test_pitchtools_get_pitch_numbers_01( ):

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   assert pitchtools.get_pitch_numbers(t) == (0, 2, 4)


def test_pitchtools_get_pitch_numbers_02( ):

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   assert pitchtools.get_pitch_numbers(t) == (0, 2, 4, 5)
