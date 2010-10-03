from abjad import *


def test_pitchtools_is_diatonic_pitch_class_name_string_01( ):

   assert pitchtools.is_diatonic_pitch_class_name_string('c')
   assert pitchtools.is_diatonic_pitch_class_name_string('d')
   assert pitchtools.is_diatonic_pitch_class_name_string('e')
   assert pitchtools.is_diatonic_pitch_class_name_string('f')
   assert pitchtools.is_diatonic_pitch_class_name_string('g')
   assert pitchtools.is_diatonic_pitch_class_name_string('a')
   assert pitchtools.is_diatonic_pitch_class_name_string('b')


def test_pitchtools_is_diatonic_pitch_class_name_string_02( ):

   assert pitchtools.is_diatonic_pitch_class_name_string('C')
   assert pitchtools.is_diatonic_pitch_class_name_string('D')
   assert pitchtools.is_diatonic_pitch_class_name_string('E')
   assert pitchtools.is_diatonic_pitch_class_name_string('F')
   assert pitchtools.is_diatonic_pitch_class_name_string('G')
   assert pitchtools.is_diatonic_pitch_class_name_string('A')
   assert pitchtools.is_diatonic_pitch_class_name_string('B')
