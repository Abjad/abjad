from abjad import *


def test_pitchtools_letter_to_diatonic_scale_degree_01( ):

   assert pitchtools.letter_to_diatonic_scale_degree('c') == 1
   assert pitchtools.letter_to_diatonic_scale_degree('d') == 2
   assert pitchtools.letter_to_diatonic_scale_degree('e') == 3
   assert pitchtools.letter_to_diatonic_scale_degree('f') == 4
   assert pitchtools.letter_to_diatonic_scale_degree('g') == 5
   assert pitchtools.letter_to_diatonic_scale_degree('a') == 6
   assert pitchtools.letter_to_diatonic_scale_degree('b') == 7

