from abjad import *


def test_pitchtools_pitch_string_to_name_01( ):

   assert pitchtools.pitch_string_to_name("cs'") == 'cs'
   assert pitchtools.pitch_string_to_name('cs') == 'cs'
   assert pitchtools.pitch_string_to_name('cs,') == 'cs'
