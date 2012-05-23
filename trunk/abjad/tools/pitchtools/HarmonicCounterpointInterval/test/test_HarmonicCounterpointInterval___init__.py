from abjad import *


def test_HarmonicCounterpointInterval___init___01():

    hcpi = pitchtools.HarmonicCounterpointInterval(10)
    assert repr(hcpi) == 'HarmonicCounterpointInterval(10)'
    assert str(hcpi) == '10'
    assert hcpi.number == 10


def test_HarmonicCounterpointInterval___init___02():
    '''Works with ascending diatonic interval instances.'''

    mdi = pitchtools.MelodicDiatonicInterval('major', 10)
    hcpi = pitchtools.HarmonicCounterpointInterval(mdi)
    assert repr(hcpi) == 'HarmonicCounterpointInterval(10)'
    assert str(hcpi) == '10'
    assert hcpi.number == 10


def test_HarmonicCounterpointInterval___init___03():
    '''Works with descending diatonic interval instances.'''

    mdi = pitchtools.MelodicDiatonicInterval('major', -10)
    hcpi = pitchtools.HarmonicCounterpointInterval(mdi)
    assert repr(hcpi) == 'HarmonicCounterpointInterval(10)'
    assert str(hcpi) == '10'
    assert hcpi.number == 10
