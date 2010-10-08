from abjad import *


def test_pitchtools_named_chromatic_pitch_tokens_to_named_chromatic_pitches_01( ):

   assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([ ]) == [ ]
   assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0]) == [pitchtools.NamedPitch(0)]
   assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0, 2, 4]) == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]


def test_pitchtools_named_chromatic_pitch_tokens_to_named_chromatic_pitches_02( ):

   assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([('df', 4)]) == [pitchtools.NamedPitch('df', 4)]
   assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([pitchtools.NamedPitch('df', 4)]) == [pitchtools.NamedPitch('df', 4)]
   assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([('df', 4), 0]) == [pitchtools.NamedPitch('df', 4), pitchtools.NamedPitch(0)]
