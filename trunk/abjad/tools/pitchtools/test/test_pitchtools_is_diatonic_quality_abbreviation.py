from abjad import *


def test_pitchtools_is_diatonic_quality_abbreviation_01():

    assert pitchtools.is_diatonic_quality_abbreviation('M')
    assert pitchtools.is_diatonic_quality_abbreviation('m')
    assert pitchtools.is_diatonic_quality_abbreviation('P')
    assert pitchtools.is_diatonic_quality_abbreviation('aug')
    assert pitchtools.is_diatonic_quality_abbreviation('dim')


def test_pitchtools_is_diatonic_quality_abbreviation_02():

    assert not pitchtools.is_diatonic_quality_abbreviation('x')
    assert not pitchtools.is_diatonic_quality_abbreviation(17)
