from abjad import *


def test_pitchtools_make_named_pitches_from_pitch_tokens_01( ):

   assert pitchtools.make_named_pitches_from_pitch_tokens([ ]) == [ ]
   assert pitchtools.make_named_pitches_from_pitch_tokens([0]) == [pitchtools.NamedPitch(0)]
   assert pitchtools.make_named_pitches_from_pitch_tokens([0, 2, 4]) == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]


def test_pitchtools_make_named_pitches_from_pitch_tokens_02( ):

   assert pitchtools.make_named_pitches_from_pitch_tokens([('df', 4)]) == [pitchtools.NamedPitch('df', 4)]
   assert pitchtools.make_named_pitches_from_pitch_tokens([pitchtools.NamedPitch('df', 4)]) == [pitchtools.NamedPitch('df', 4)]
   assert pitchtools.make_named_pitches_from_pitch_tokens([('df', 4), 0]) == [pitchtools.NamedPitch('df', 4), pitchtools.NamedPitch(0)]
