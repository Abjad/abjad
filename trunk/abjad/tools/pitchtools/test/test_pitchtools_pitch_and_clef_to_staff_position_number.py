from abjad import *


def test_pitchtools_pitch_and_clef_to_staff_position_number_01( ):

   clef = Clef('treble')

   pitch = Pitch('c', 4)
   number = pitchtools.pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == -6

   pitch = Pitch('d', 4)
   number = pitchtools.pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == -5

   pitch = Pitch('e', 4)
   number = pitchtools.pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == -4


def test_pitchtools_pitch_and_clef_to_staff_position_number_02( ):

   clef = Clef('alto')

   pitch = Pitch('c', 4)
   number = pitchtools.pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == 0

   pitch = Pitch('d', 4)
   number = pitchtools.pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == 1

   pitch = Pitch('e', 4)
   number = pitchtools.pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == 2
