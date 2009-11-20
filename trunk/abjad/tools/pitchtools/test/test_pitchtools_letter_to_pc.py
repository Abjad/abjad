from abjad import *


def test_pitchtools_letter_to_pc_01( ):


   assert pitchtools.letter_to_pc('c') == 0
   assert pitchtools.letter_to_pc('d') == 2
   assert pitchtools.letter_to_pc('e') == 4
   assert pitchtools.letter_to_pc('f') == 5
   assert pitchtools.letter_to_pc('g') == 7
   assert pitchtools.letter_to_pc('a') == 9
   assert pitchtools.letter_to_pc('b') == 11
