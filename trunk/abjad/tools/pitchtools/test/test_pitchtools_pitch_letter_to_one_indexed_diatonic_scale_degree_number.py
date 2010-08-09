from abjad import *


def test_pitchtools_pitch_letter_to_one_indexed_diatonic_scale_degree_number_01( ):

   assert pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number('c') == 1
   assert pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number('d') == 2
   assert pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number('e') == 3
   assert pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number('f') == 4
   assert pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number('g') == 5
   assert pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number('a') == 6
   assert pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number('b') == 7

