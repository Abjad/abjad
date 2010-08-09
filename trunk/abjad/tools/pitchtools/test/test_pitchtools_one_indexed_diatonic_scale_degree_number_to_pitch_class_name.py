from abjad import *


def test_pitchtools_one_indexed_diatonic_scale_degree_number_to_pitch_class_name_01( ):

   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(1) == 'c'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(2) == 'd'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(3) == 'e'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(4) == 'f'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(5) == 'g'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(6) == 'a'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(7) == 'b'


def test_pitchtools_one_indexed_diatonic_scale_degree_number_to_pitch_class_name_02( ):

   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(8) == 'c'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(9) == 'd'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(10) == 'e'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(11) == 'f'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(12) == 'g'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(13) == 'a'
   assert pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name(14) == 'b'
