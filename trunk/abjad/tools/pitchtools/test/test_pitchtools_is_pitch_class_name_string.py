from abjad import *


def test_pitchtools_is_pitch_class_name_string_01( ):

   assert pitchtools.is_pitch_class_name_string('c')
   assert pitchtools.is_pitch_class_name_string('cs')
   assert pitchtools.is_pitch_class_name_string('css')
   assert pitchtools.is_pitch_class_name_string('cqs')
   assert pitchtools.is_pitch_class_name_string('ctqs')
   assert pitchtools.is_pitch_class_name_string('cf')
   assert pitchtools.is_pitch_class_name_string('cff')
   assert pitchtools.is_pitch_class_name_string('cqf')
   assert pitchtools.is_pitch_class_name_string('ctqf')


def test_pitchtools_is_pitch_class_name_string_02( ):

   assert not pitchtools.is_pitch_class_name_string('c,')
   assert not pitchtools.is_pitch_class_name_string("c'")
