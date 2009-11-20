from abjad import *


def test_pitchtools_diatonic_scale_degree_to_letter_01( ):

   assert pitchtools.diatonic_scale_degree_to_letter(1) == 'c'
   assert pitchtools.diatonic_scale_degree_to_letter(2) == 'd'
   assert pitchtools.diatonic_scale_degree_to_letter(3) == 'e'
   assert pitchtools.diatonic_scale_degree_to_letter(4) == 'f'
   assert pitchtools.diatonic_scale_degree_to_letter(5) == 'g'
   assert pitchtools.diatonic_scale_degree_to_letter(6) == 'a'
   assert pitchtools.diatonic_scale_degree_to_letter(7) == 'b'
