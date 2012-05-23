from abjad import *


def test_HarmonicDiatonicInterval___init___01():
    '''Init harmonic diatonic interval from abbreviation.
    '''

    hdi = pitchtools.HarmonicDiatonicInterval('M3')

    assert hdi.quality_string == 'major'
    assert hdi.number == 3


def test_HarmonicDiatonicInterval___init___02():
    '''Can init from quality string and interval number.'''

    hdi = pitchtools.HarmonicDiatonicInterval('major', 3)

    assert hdi.quality_string == 'major'
    assert hdi.number == 3


def test_HarmonicDiatonicInterval___init___03():
    '''Can init from other harmonic diatonic interval.'''

    hdi = pitchtools.HarmonicDiatonicInterval('major', 3)
    new = pitchtools.HarmonicDiatonicInterval(hdi)

    assert hdi.quality_string == 'major'
    assert hdi.number == 3

    assert new.quality_string == 'major'
    assert new.number == 3

    assert new is not hdi
    assert new == hdi


def test_HarmonicDiatonicInterval___init___04():
    '''Can init from melodic diatonic interval.'''

    mdi = pitchtools.MelodicDiatonicInterval('major', -3)
    hdi = pitchtools.HarmonicDiatonicInterval(mdi)

    assert mdi.quality_string == 'major'
    assert mdi.number == -3

    assert hdi.quality_string == 'major'
    assert hdi.number == 3

    assert hdi is not mdi
    assert not hdi == mdi
