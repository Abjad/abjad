from abjad import *


def test_pitchtools_diatonic_scale_degree_to_letter_01( ):

   assert pitchtools.diatonic_scale_degree_to_letter(1) == 'c'
   assert pitchtools.diatonic_scale_degree_to_letter(2) == 'd'
   assert pitchtools.diatonic_scale_degree_to_letter(3) == 'e'
   assert pitchtools.diatonic_scale_degree_to_letter(4) == 'f'
   assert pitchtools.diatonic_scale_degree_to_letter(5) == 'g'
   assert pitchtools.diatonic_scale_degree_to_letter(6) == 'a'
   assert pitchtools.diatonic_scale_degree_to_letter(7) == 'b'


def test_pitchtools_diatonic_scale_degree_to_letter_02( ):

   assert pitchtools.diatonic_scale_degree_to_letter(8) == 'c'
   assert pitchtools.diatonic_scale_degree_to_letter(9) == 'd'
   assert pitchtools.diatonic_scale_degree_to_letter(10) == 'e'
   assert pitchtools.diatonic_scale_degree_to_letter(11) == 'f'
   assert pitchtools.diatonic_scale_degree_to_letter(12) == 'g'
   assert pitchtools.diatonic_scale_degree_to_letter(13) == 'a'
   assert pitchtools.diatonic_scale_degree_to_letter(14) == 'b'
