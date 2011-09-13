from abjad import *


def test_pitchtools_calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_01():
    '''Ascending intervals greater than an octave.'''

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_pitchtools_calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_02():
    '''Ascending octave.'''

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)


def test_pitchtools_calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_03():
    '''Ascending intervals less than an octave.'''

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_pitchtools_calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_04():
    '''Unison.'''

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 1)


def test_pitchtools_calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_05():
    '''Descending intervals greater than an octave.'''

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_pitchtools_calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_06():
    '''Descending octave.'''

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)


def test_pitchtools_calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_07():
    '''Descending intervals less than an octave.'''

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)
