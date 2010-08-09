from abjad import *


def test_pitchtools_pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair_01( ):

   assert pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair('c') == ('c', '')
   assert pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair('cs') == ('c', 's')
   assert pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair('d') == ('d', '')
   assert pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair('ds') == ('d', 's')

