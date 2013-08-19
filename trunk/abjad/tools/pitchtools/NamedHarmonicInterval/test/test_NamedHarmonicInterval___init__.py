# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval___init___01():
    r'''Init harmonic diatonic interval from abbreviation.
    '''

    hdi = pitchtools.NamedHarmonicInterval('M3')

    assert hdi.quality_string == 'major'
    assert hdi.number == 3


def test_NamedHarmonicInterval___init___02():
    r'''Can init from quality string and interval number.
    '''

    hdi = pitchtools.NamedHarmonicInterval('major', 3)

    assert hdi.quality_string == 'major'
    assert hdi.number == 3


def test_NamedHarmonicInterval___init___03():
    r'''Can init from other harmonic diatonic interval.
    '''

    hdi = pitchtools.NamedHarmonicInterval('major', 3)
    new = pitchtools.NamedHarmonicInterval(hdi)

    assert hdi.quality_string == 'major'
    assert hdi.number == 3

    assert new.quality_string == 'major'
    assert new.number == 3

    assert new is not hdi
    assert new == hdi


def test_NamedHarmonicInterval___init___04():
    r'''Can init from melodic diatonic interval.
    '''

    mdi = pitchtools.NamedMelodicInterval('major', -3)
    hdi = pitchtools.NamedHarmonicInterval(mdi)

    assert mdi.quality_string == 'major'
    assert mdi.number == -3

    assert hdi.quality_string == 'major'
    assert hdi.number == 3

    assert hdi is not mdi
    assert not hdi == mdi
