from abjad import *


def test_pitchtools_list_chromatic_pitch_numbers_in_expr_01( ):

   t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   assert pitchtools.list_chromatic_pitch_numbers_in_expr(t) == (0, 2, 4)


def test_pitchtools_list_chromatic_pitch_numbers_in_expr_02( ):

   t = Staff(macros.scale(4))
   assert pitchtools.list_chromatic_pitch_numbers_in_expr(t) == (0, 2, 4, 5)
