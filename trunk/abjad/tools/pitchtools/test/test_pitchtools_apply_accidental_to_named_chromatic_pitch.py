from abjad import *


def test_pitchtools_apply_accidental_to_named_chromatic_pitch_01():

    assert pitchtools.apply_accidental_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch('cs', 4), 'sharp') == pitchtools.NamedChromaticPitch('css', 4)
    assert pitchtools.apply_accidental_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch('cs', 4), 'flat') == pitchtools.NamedChromaticPitch('c', 4)
    assert pitchtools.apply_accidental_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch('cs', 4), 'natural') == pitchtools.NamedChromaticPitch('cs', 4)
    assert pitchtools.apply_accidental_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch('cs', 4), 'quarter sharp') == pitchtools.NamedChromaticPitch('ctqs', 4)
