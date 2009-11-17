from abjad import *


def test_pitchtools_get_pitch_numbers_01( ):

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   assert pitchtools.get_pitch_numbers(t) == (0, 2, 4)


def test_pitchtools_get_pitch_numbers_02( ):

   t = Staff(construct.scale(4))
   assert pitchtools.get_pitch_numbers(t) == (0, 2, 4, 5)
