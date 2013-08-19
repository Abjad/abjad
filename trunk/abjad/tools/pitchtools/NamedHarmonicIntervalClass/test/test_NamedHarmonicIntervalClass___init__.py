# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicIntervalClass___init___01():
    r'''Unisons and octaves are treated differently.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass('perfect', 1)
    assert str(hdic) == 'P1'
    assert hdic.number == 1

    hdic = pitchtools.NamedHarmonicIntervalClass('perfect', -1)
    assert str(hdic) == 'P1'
    assert hdic.number == 1


def test_NamedHarmonicIntervalClass___init___02():
    r'''Unisons and octaves are treated differently.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass('perfect', -15)
    assert str(hdic) == 'P8'
    assert hdic.number == 8

    hdic = pitchtools.NamedHarmonicIntervalClass('perfect', -8)
    assert str(hdic) == 'P8'
    assert hdic.number == 8

    hdic = pitchtools.NamedHarmonicIntervalClass('perfect', 8)
    assert str(hdic) == 'P8'
    assert hdic.number == 8

    hdic = pitchtools.NamedHarmonicIntervalClass('perfect', 15)
    assert str(hdic) == 'P8'
    assert hdic.number == 8


def test_NamedHarmonicIntervalClass___init___03():
    r'''Works on harmonic diatonic interval instances.
    '''

    hdi = pitchtools.NamedHarmonicInterval('perfect', 15)
    hdic = pitchtools.NamedHarmonicIntervalClass(hdi)
    assert str(hdic) == 'P8'
    assert hdic.number == 8


def test_NamedHarmonicIntervalClass___init___04():
    r'''Works on sevenths.
    '''

    hdi = pitchtools.NamedHarmonicInterval('minor', -14)
    hdic = pitchtools.NamedHarmonicIntervalClass(hdi)
    assert str(hdic) == 'm7'
    assert hdic.number == 7

    hdi = pitchtools.NamedHarmonicInterval('minor', -7)
    hdic = pitchtools.NamedHarmonicIntervalClass(hdi)
    assert str(hdic) == 'm7'
    assert hdic.number == 7

    hdi = pitchtools.NamedHarmonicInterval('minor', 7)
    hdic = pitchtools.NamedHarmonicIntervalClass(hdi)
    assert str(hdic) == 'm7'
    assert hdic.number == 7

    hdi = pitchtools.NamedHarmonicInterval('minor', 14)
    hdic = pitchtools.NamedHarmonicIntervalClass(hdi)
    assert str(hdic) == 'm7'
    assert hdic.number == 7
