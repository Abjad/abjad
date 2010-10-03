from abjad import *


def test_pitchtools_is_diatonic_pitch_name_string_with_octave_ticks_01( ):

   assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks("c,,,")
   assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks("c,,")
   assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks("c,")
   assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks("c")
   assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks("c'")
   assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks("c'")
   assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks("c''")


def test_pitchtools_is_diatonic_pitch_name_string_with_octave_ticks_02( ):

   assert not pitchtools.is_diatonic_pitch_name_string_with_octave_ticks('cs')
