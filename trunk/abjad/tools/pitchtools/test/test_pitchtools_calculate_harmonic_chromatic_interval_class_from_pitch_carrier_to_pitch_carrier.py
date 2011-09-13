from abjad import *


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_01():
    '''Ascending intervals greater than an octave.'''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_02():
    '''Ascending octave.'''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_03():
    '''Ascending intervals less than an octave.'''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_04():
    '''Unison.'''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(0)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_05():
    '''Descending intervals greater than an octave.'''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_06():
    '''Descending octave.'''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_07():
    '''Descending intervals less than an octave.'''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_08():
    '''Works with quartertones.'''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2.5))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2.5)
