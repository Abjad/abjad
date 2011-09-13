from abjad import *


def test_pitchtools_is_named_chromatic_pitch_token_01():

    assert pitchtools.is_named_chromatic_pitch_token(('cs', 4))
    assert pitchtools.is_named_chromatic_pitch_token(pitchtools.NamedChromaticPitch('cs', 4))
    assert pitchtools.is_named_chromatic_pitch_token(1)
    assert pitchtools.is_named_chromatic_pitch_token(1.0)


def test_pitchtools_is_named_chromatic_pitch_token_02():

    assert not pitchtools.is_named_chromatic_pitch_token('foo')
