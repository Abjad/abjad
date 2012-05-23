from abjad import *


def test_MelodicChromaticInterval___init___01():
    '''Init from positive number.'''

    i = pitchtools.MelodicChromaticInterval(3)
    assert i.number == 3


def test_MelodicChromaticInterval___init___02():
    '''Init from negative number.'''

    i = pitchtools.MelodicChromaticInterval(-3)
    assert i.number == -3


def test_MelodicChromaticInterval___init___03():
    '''Init from other chromatic interval.'''

    i = pitchtools.MelodicChromaticInterval(3)
    j = pitchtools.MelodicChromaticInterval(i)
    assert i.number == j.number == 3
    assert i is not j


def test_MelodicChromaticInterval___init___04():
    '''Init from melodic diatonic interval.'''

    diatonic_interval = pitchtools.MelodicDiatonicInterval('perfect', 4)
    i = pitchtools.MelodicChromaticInterval(diatonic_interval)
    assert i.number == 5
