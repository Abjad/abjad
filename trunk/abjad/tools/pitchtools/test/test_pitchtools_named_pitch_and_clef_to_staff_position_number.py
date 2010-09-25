from abjad import *


def test_pitchtools_named_pitch_and_clef_to_staff_position_number_01( ):

   clef = marktools.ClefMark('treble')

   pitch = pitchtools.NamedPitch('c', 4)
   number = pitchtools.named_pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == -6

   pitch = pitchtools.NamedPitch('d', 4)
   number = pitchtools.named_pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == -5

   pitch = pitchtools.NamedPitch('e', 4)
   number = pitchtools.named_pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == -4


def test_pitchtools_named_pitch_and_clef_to_staff_position_number_02( ):

   clef = marktools.ClefMark('alto')

   pitch = pitchtools.NamedPitch('c', 4)
   number = pitchtools.named_pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == 0

   pitch = pitchtools.NamedPitch('d', 4)
   number = pitchtools.named_pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == 1

   pitch = pitchtools.NamedPitch('e', 4)
   number = pitchtools.named_pitch_and_clef_to_staff_position_number(pitch, clef)
   assert number == 2
