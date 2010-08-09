from abjad import *


def test_pitchtools_transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number_01( ):

   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 0) == 12
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 1) == 13
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 2) == 14 
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 3) == 15
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 4) == 16
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 5) == 17


def test_pitchtools_transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number_02( ):

   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 6) == 6
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 7) == 7
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 8) == 8
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 9) == 9
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 10) == 10
   assert pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 11) == 11
