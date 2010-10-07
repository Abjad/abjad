from abjad import *


def test_pitchtools_chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_string_pair_01( ):

   assert pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_string_pair('c') == ('c', '')
   assert pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_string_pair('cs') == ('c', 's')
   assert pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_string_pair('d') == ('d', '')
   assert pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_string_pair('ds') == ('d', 's')

