from abjad import *


def test_pitchtools_calculate_harmonic_diatonic_interval_01():

    pitch = pitchtools.NamedChromaticPitch(12)

    interval = pitchtools.calculate_harmonic_diatonic_interval(pitch, pitchtools.NamedChromaticPitch(12))
    assert interval == pitchtools.HarmonicDiatonicInterval('perfect', 1)

    interval = pitchtools.calculate_harmonic_diatonic_interval(
        pitch, pitchtools.NamedChromaticPitch('b', 4))
    assert interval == pitchtools.HarmonicDiatonicInterval('minor', 2)

    interval = pitchtools.calculate_harmonic_diatonic_interval(
        pitch, pitchtools.NamedChromaticPitch('bf', 4))
    assert interval == pitchtools.HarmonicDiatonicInterval('major', 2)

    interval = pitchtools.calculate_harmonic_diatonic_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch('as', 4))
    assert interval == pitchtools.HarmonicDiatonicInterval('diminished', 3)


def test_pitchtools_calculate_harmonic_diatonic_interval_02():

    pitch = pitchtools.NamedChromaticPitch(12)

    interval = pitchtools.calculate_harmonic_diatonic_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch('a', 4))
    assert interval == pitchtools.HarmonicDiatonicInterval('minor', 3)

    interval = pitchtools.calculate_harmonic_diatonic_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch('af', 4))
    assert interval == pitchtools.HarmonicDiatonicInterval('major', 3)

    interval = pitchtools.calculate_harmonic_diatonic_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch('gs', 4))
    assert interval == pitchtools.HarmonicDiatonicInterval('diminished', 4)

    interval = pitchtools.calculate_harmonic_diatonic_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch('g', 4))
    assert interval == pitchtools.HarmonicDiatonicInterval('perfect', 4)
