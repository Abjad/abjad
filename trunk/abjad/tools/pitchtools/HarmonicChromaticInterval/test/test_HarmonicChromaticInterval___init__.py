from abjad import *


def test_HarmonicChromaticInterval___init___01():
    r'''Init from positive number.
    '''

    i = pitchtools.HarmonicChromaticInterval(3)
    assert i.number == 3


def test_HarmonicChromaticInterval___init___02():
    r'''Init from negative number.
    '''

    i = pitchtools.HarmonicChromaticInterval(-3)
    assert i.number == 3


def test_HarmonicChromaticInterval___init___03():
    r'''Init from other harmonic chromatic interval.
    '''

    i = pitchtools.HarmonicChromaticInterval(3)
    j = pitchtools.HarmonicChromaticInterval(i)
    assert i.number == j.number == 3
    assert i is not j


def test_HarmonicChromaticInterval___init___04():
    r'''Init from melodic diatonic interval.
    '''

    diatonic_interval = pitchtools.MelodicDiatonicInterval('perfect', 4)
    i = pitchtools.HarmonicChromaticInterval(diatonic_interval)
    assert i.number == 5
