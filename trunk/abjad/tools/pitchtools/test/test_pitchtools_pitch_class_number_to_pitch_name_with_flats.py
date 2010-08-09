from abjad import *


def test_pitchtools_pitch_class_number_to_pitch_name_with_flats_01( ):

   assert pitchtools.pitch_class_number_to_pitch_name_with_flats(0) == 'c'
   assert pitchtools.pitch_class_number_to_pitch_name_with_flats(0.5) == 'dtqf'
   assert pitchtools.pitch_class_number_to_pitch_name_with_flats(1) == 'df'
   assert pitchtools.pitch_class_number_to_pitch_name_with_flats(1.5) == 'dqf'
   assert pitchtools.pitch_class_number_to_pitch_name_with_flats(2) == 'd'
   assert pitchtools.pitch_class_number_to_pitch_name_with_flats(2.5) == 'etqf'
