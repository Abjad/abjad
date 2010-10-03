from abjad import *


def test_pitchtools_is_pitch_name_string_with_octave_ticks_01( ):

   assert pitchtools.is_pitch_name_string_with_octave_ticks('c,')
   assert pitchtools.is_pitch_name_string_with_octave_ticks('cs,')
   assert pitchtools.is_pitch_name_string_with_octave_ticks('c')
   assert pitchtools.is_pitch_name_string_with_octave_ticks('cs')


def test_pitchtools_is_pitch_name_string_with_octave_ticks_02( ):

   assert not pitchtools.is_pitch_name_string_with_octave_ticks('foo')
   assert not pitchtools.is_pitch_name_string_with_octave_ticks('c4')
