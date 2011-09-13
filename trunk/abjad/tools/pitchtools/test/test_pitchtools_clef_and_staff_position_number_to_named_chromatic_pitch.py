from abjad import *


def test_pitchtools_clef_and_staff_position_number_to_named_chromatic_pitch_01():

    clef = contexttools.ClefMark('treble')

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, -1)
    assert pitch == pitchtools.NamedChromaticPitch('a', 4)

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, 0)
    assert pitch == pitchtools.NamedChromaticPitch('b', 4)

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, 1)
    assert pitch == pitchtools.NamedChromaticPitch('c', 5)


def test_pitchtools_clef_and_staff_position_number_to_named_chromatic_pitch_02():

    clef = contexttools.ClefMark('alto')

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, -1)
    assert pitch == pitchtools.NamedChromaticPitch('b', 3)

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, 0)
    assert pitch == pitchtools.NamedChromaticPitch('c', 4)

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, 1)
    assert pitch == pitchtools.NamedChromaticPitch('d', 4)


def test_pitchtools_clef_and_staff_position_number_to_named_chromatic_pitch_03():

    clef = contexttools.ClefMark('bass')

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, -1)
    assert pitch == pitchtools.NamedChromaticPitch('c', 3)

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, 0)
    assert pitch == pitchtools.NamedChromaticPitch('d', 3)

    pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, 1)
    assert pitch == pitchtools.NamedChromaticPitch('e', 3)
