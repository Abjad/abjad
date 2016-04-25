# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval___init___01():
    r'''Initialize named interval from abbreviation.
    '''

    mdi = pitchtools.NamedInterval('+M3')
    assert mdi.quality_string == 'major'
    assert mdi.number == 3


def test_pitchtools_NamedInterval___init___02():
    r'''Can init from quality string and interval number.
    '''

    mdi = pitchtools.NamedInterval('major', 3)
    assert mdi.quality_string == 'major'
    assert mdi.number == 3


def test_pitchtools_NamedInterval___init___03():
    r'''Can init from other named interval instance.
    '''

    mdi = pitchtools.NamedInterval('major', 3)
    new = pitchtools.NamedInterval(mdi)

    assert mdi.quality_string == 'major'
    assert mdi.number == 3

    assert new.quality_string == 'major'
    assert new.number == 3

    assert new is not mdi
    assert new == mdi
