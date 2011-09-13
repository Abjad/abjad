from abjad import *


def test_pitchtools_calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier_01():
    '''Ascending intervals greater than an octave.'''

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert hci == pitchtools.HarmonicChromaticInterval(15)

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert hci == pitchtools.HarmonicChromaticInterval(14)

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert hci == pitchtools.HarmonicChromaticInterval(13)


def test_pitchtools_calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier_02():
    '''Ascending octave.'''

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert hci == pitchtools.HarmonicChromaticInterval(12)


def test_pitchtools_calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier_03():
    '''Ascending intervals less than an octave.'''

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert hci == pitchtools.HarmonicChromaticInterval(3)

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert hci == pitchtools.HarmonicChromaticInterval(2)

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert hci == pitchtools.HarmonicChromaticInterval(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier_04():
    '''Unison.'''

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert hci == pitchtools.HarmonicChromaticInterval(0)


def test_pitchtools_calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier_05():
    '''Descending intervals greater than an octave.'''

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert hci == pitchtools.HarmonicChromaticInterval(15)

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert hci == pitchtools.HarmonicChromaticInterval(14)

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert hci == pitchtools.HarmonicChromaticInterval(13)


def test_pitchtools_calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier_06():
    '''Descending octave.'''

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert hci == pitchtools.HarmonicChromaticInterval(12)


def test_pitchtools_calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier_07():
    '''Descending intervals less than an octave.'''

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert hci == pitchtools.HarmonicChromaticInterval(3)

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert hci == pitchtools.HarmonicChromaticInterval(2)

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert hci == pitchtools.HarmonicChromaticInterval(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier_08():
    '''Works with quartertones.'''

    hci = pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2.5))
    assert hci == pitchtools.HarmonicChromaticInterval(14.5)
