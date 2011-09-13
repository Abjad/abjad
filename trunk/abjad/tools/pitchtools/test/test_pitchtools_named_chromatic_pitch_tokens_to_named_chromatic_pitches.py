from abjad import *


def test_pitchtools_named_chromatic_pitch_tokens_to_named_chromatic_pitches_01():

    assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([]) == []
    assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0]) == [pitchtools.NamedChromaticPitch(0)]
    assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0, 2, 4]) == [pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4)]


def test_pitchtools_named_chromatic_pitch_tokens_to_named_chromatic_pitches_02():

    assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([('df', 4)]) == [pitchtools.NamedChromaticPitch('df', 4)]
    assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([pitchtools.NamedChromaticPitch('df', 4)]) == [pitchtools.NamedChromaticPitch('df', 4)]
    assert pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([('df', 4), 0]) == [pitchtools.NamedChromaticPitch('df', 4), pitchtools.NamedChromaticPitch(0)]
