from abjad import *
import py.test


def test_pitchtools_transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell_01():

    pitch = pitchtools.NamedChromaticPitch(0)

    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 0) == pitchtools.NamedChromaticPitch('dff', 4)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 0.5) == pitchtools.NamedChromaticPitch('dtqf', 4)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 1) == pitchtools.NamedChromaticPitch('df', 4)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 1.5) == pitchtools.NamedChromaticPitch('dqf', 4)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 2) == pitchtools.NamedChromaticPitch('d', 4)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 2.5) == pitchtools.NamedChromaticPitch('dqs', 4)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 3) == pitchtools.NamedChromaticPitch('ds', 4)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 3.5) == pitchtools.NamedChromaticPitch('dtqs', 4)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 4) == pitchtools.NamedChromaticPitch('dss', 4)

    assert py.test.raises(
        KeyError, 'pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 4.5)')


def test_pitchtools_transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell_02():

    pitch = pitchtools.NamedChromaticPitch(0)

    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, 0) == pitchtools.NamedChromaticPitch('bs', 3)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -0.5) == pitchtools.NamedChromaticPitch('bqs', 3)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -1) == pitchtools.NamedChromaticPitch('b', 3)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -1.5) == pitchtools.NamedChromaticPitch('bqf', 3)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -2) == pitchtools.NamedChromaticPitch('bf', 3)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -2.5) == pitchtools.NamedChromaticPitch('btqf', 3)
    assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -3) == pitchtools.NamedChromaticPitch('bff', 3)
