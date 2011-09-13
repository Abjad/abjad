from abjad import *


def test_HarmonicDiatonicIntervalClass___init___01():
    '''Unisons and octaves are treated differently.'''

    hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', 1)
    assert str(hdic) == 'P1'
    assert hdic.number == 1

    hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', -1)
    assert str(hdic) == 'P1'
    assert hdic.number == 1


def test_HarmonicDiatonicIntervalClass___init___02():
    '''Unisons and octaves are treated differently.'''

    hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', -15)
    assert str(hdic) == 'P8'
    assert hdic.number == 8

    hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', -8)
    assert str(hdic) == 'P8'
    assert hdic.number == 8

    hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)
    assert str(hdic) == 'P8'
    assert hdic.number == 8

    hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', 15)
    assert str(hdic) == 'P8'
    assert hdic.number == 8


def test_HarmonicDiatonicIntervalClass___init___03():
    '''Works on harmonic diatonic interval instances.'''

    hdi = pitchtools.HarmonicDiatonicInterval('perfect', 15)
    hdic = pitchtools.HarmonicDiatonicIntervalClass(hdi)
    assert str(hdic) == 'P8'
    assert hdic.number == 8


def test_HarmonicDiatonicIntervalClass___init___04():
    '''Works on sevenths.'''

    hdi = pitchtools.HarmonicDiatonicInterval('minor', -14)
    hdic = pitchtools.HarmonicDiatonicIntervalClass(hdi)
    assert str(hdic) == 'm7'
    assert hdic.number == 7

    hdi = pitchtools.HarmonicDiatonicInterval('minor', -7)
    hdic = pitchtools.HarmonicDiatonicIntervalClass(hdi)
    assert str(hdic) == 'm7'
    assert hdic.number == 7

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 7)
    hdic = pitchtools.HarmonicDiatonicIntervalClass(hdi)
    assert str(hdic) == 'm7'
    assert hdic.number == 7

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 14)
    hdic = pitchtools.HarmonicDiatonicIntervalClass(hdi)
    assert str(hdic) == 'm7'
    assert hdic.number == 7
