from abjad import *


def test_pitchtools_is_harmonic_diatonic_interval_abbreviation_01():

    assert pitchtools.is_harmonic_diatonic_interval_abbreviation('M2')
    assert pitchtools.is_harmonic_diatonic_interval_abbreviation('M9')
    assert pitchtools.is_harmonic_diatonic_interval_abbreviation('M16')
    assert pitchtools.is_harmonic_diatonic_interval_abbreviation('aug2')
    assert pitchtools.is_harmonic_diatonic_interval_abbreviation('aug9')
    assert pitchtools.is_harmonic_diatonic_interval_abbreviation('aug16')


def test_pitchtools_is_harmonic_diatonic_interval_abbreviation_02():

    assert not pitchtools.is_harmonic_diatonic_interval_abbreviation('+M2')
    assert not pitchtools.is_harmonic_diatonic_interval_abbreviation('-M2')
    assert not pitchtools.is_harmonic_diatonic_interval_abbreviation('x2')
    assert not pitchtools.is_harmonic_diatonic_interval_abbreviation(17)
