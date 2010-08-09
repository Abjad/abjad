from abjad import *


def test_pitchtools_pitch_name_to_pitch_class_name_01( ):

   assert pitchtools.pitch_name_to_pitch_class_name("cs'") == 'cs'
   assert pitchtools.pitch_name_to_pitch_class_name('cs') == 'cs'
   assert pitchtools.pitch_name_to_pitch_class_name('cs,') == 'cs'
