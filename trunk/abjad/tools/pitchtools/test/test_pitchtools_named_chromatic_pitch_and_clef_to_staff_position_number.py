from abjad import *


def test_pitchtools_named_chromatic_pitch_and_clef_to_staff_position_number_01():

    clef = contexttools.ClefMark('treble')

    pitch = pitchtools.NamedChromaticPitch('c', 4)
    number = pitchtools.named_chromatic_pitch_and_clef_to_staff_position_number(pitch, clef)
    assert number == -6

    pitch = pitchtools.NamedChromaticPitch('d', 4)
    number = pitchtools.named_chromatic_pitch_and_clef_to_staff_position_number(pitch, clef)
    assert number == -5

    pitch = pitchtools.NamedChromaticPitch('e', 4)
    number = pitchtools.named_chromatic_pitch_and_clef_to_staff_position_number(pitch, clef)
    assert number == -4


def test_pitchtools_named_chromatic_pitch_and_clef_to_staff_position_number_02():

    clef = contexttools.ClefMark('alto')

    pitch = pitchtools.NamedChromaticPitch('c', 4)
    number = pitchtools.named_chromatic_pitch_and_clef_to_staff_position_number(pitch, clef)
    assert number == 0

    pitch = pitchtools.NamedChromaticPitch('d', 4)
    number = pitchtools.named_chromatic_pitch_and_clef_to_staff_position_number(pitch, clef)
    assert number == 1

    pitch = pitchtools.NamedChromaticPitch('e', 4)
    number = pitchtools.named_chromatic_pitch_and_clef_to_staff_position_number(pitch, clef)
    assert number == 2
