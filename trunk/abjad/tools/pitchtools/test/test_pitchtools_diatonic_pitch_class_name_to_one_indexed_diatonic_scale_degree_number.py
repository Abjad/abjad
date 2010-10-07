from abjad import *


def test_pitchtools_diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number_01( ):

   assert pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('c') == 1
   assert pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('d') == 2
   assert pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('e') == 3
   assert pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('f') == 4
   assert pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('g') == 5
   assert pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('a') == 6
   assert pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('b') == 7

