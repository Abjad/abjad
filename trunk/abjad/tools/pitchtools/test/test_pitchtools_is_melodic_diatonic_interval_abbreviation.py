from abjad import *


def test_pitchtools_is_melodic_diatonic_interval_abbreviation_01():

    assert pitchtools.is_melodic_diatonic_interval_abbreviation('+M2')
    assert pitchtools.is_melodic_diatonic_interval_abbreviation('+M9')
    assert pitchtools.is_melodic_diatonic_interval_abbreviation('+M16')
    assert pitchtools.is_melodic_diatonic_interval_abbreviation('-M2')
    assert pitchtools.is_melodic_diatonic_interval_abbreviation('-M9')
    assert pitchtools.is_melodic_diatonic_interval_abbreviation('-M16')


def test_pitchtools_is_melodic_diatonic_interval_abbreviation_02():

    assert not pitchtools.is_melodic_diatonic_interval_abbreviation(' M2')
