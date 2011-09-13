from abjad import *


def test_pitchtools_calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_01():
    '''Ascending intervals greater than an octave.'''

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', 3)

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('major', 2)

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', 2)


def test_pitchtools_calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_02():
    '''Ascending octave.'''

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('perfect', 8)


def test_pitchtools_calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_03():
    '''Ascending intervals less than an octave.'''

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', 3)

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('major', 2)

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', 2)


def test_pitchtools_calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_04():
    '''Unison.'''

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('perfect', 1)


def test_pitchtools_calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_05():
    '''Descending intervals greater than an octave.'''

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', -3)

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('major', -2)

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', -2)


def test_pitchtools_calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_06():
    '''Descending octave.'''

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('perfect', -8)


def test_pitchtools_calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch_07():
    '''Descending intervals less than an octave.'''

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', -3)

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('major', -2)

    mcpi = pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', -2)
