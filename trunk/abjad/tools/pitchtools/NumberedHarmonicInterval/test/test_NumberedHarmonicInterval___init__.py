# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedHarmonicInterval___init___01():
    r'''Init from positive number.
    '''

    i = pitchtools.NumberedHarmonicInterval(3)
    assert i.number == 3


def test_NumberedHarmonicInterval___init___02():
    r'''Init from negative number.
    '''

    i = pitchtools.NumberedHarmonicInterval(-3)
    assert i.number == 3


def test_NumberedHarmonicInterval___init___03():
    r'''Init from other harmonic chromatic interval.
    '''

    i = pitchtools.NumberedHarmonicInterval(3)
    j = pitchtools.NumberedHarmonicInterval(i)
    assert i.number == j.number == 3
    assert i is not j


def test_NumberedHarmonicInterval___init___04():
    r'''Init from melodic diatonic interval.
    '''

    diatonic_interval = pitchtools.NamedMelodicInterval('perfect', 4)
    i = pitchtools.NumberedHarmonicInterval(diatonic_interval)
    assert i.number == 5
