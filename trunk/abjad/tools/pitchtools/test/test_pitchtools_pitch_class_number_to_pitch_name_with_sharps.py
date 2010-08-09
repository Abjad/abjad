from abjad import *


def test_pitchtools_pitch_class_number_to_pitch_name_with_sharps_01( ):

   assert pitchtools.pitch_class_number_to_pitch_name_with_sharps(0) == 'c'
   assert pitchtools.pitch_class_number_to_pitch_name_with_sharps(0.5) == 'cqs'
   assert pitchtools.pitch_class_number_to_pitch_name_with_sharps(1) == 'cs'
   assert pitchtools.pitch_class_number_to_pitch_name_with_sharps(1.5) == 'ctqs'
   assert pitchtools.pitch_class_number_to_pitch_name_with_sharps(2) == 'd'
   assert pitchtools.pitch_class_number_to_pitch_name_with_sharps(2.5) == 'dqs'
