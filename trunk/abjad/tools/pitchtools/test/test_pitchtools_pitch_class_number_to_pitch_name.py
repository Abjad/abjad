from abjad import *


def test_pitchtools_pitch_class_number_to_pitch_name_01( ):

   assert pitchtools.pitch_class_number_to_pitch_name(0) == 'c'   
   assert pitchtools.pitch_class_number_to_pitch_name(0.5) == 'cqs'   
   assert pitchtools.pitch_class_number_to_pitch_name(1) == 'cs'   
   assert pitchtools.pitch_class_number_to_pitch_name(1.5) == 'dqf'   
   assert pitchtools.pitch_class_number_to_pitch_name(2) == 'd'   
   assert pitchtools.pitch_class_number_to_pitch_name(2.5) == 'dqs'   
