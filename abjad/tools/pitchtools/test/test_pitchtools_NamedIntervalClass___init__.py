# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedIntervalClass___init___01():
    r'''Unisons and octaves are treated differently.
    '''

    mdic = pitchtools.NamedIntervalClass('perfect', -15)
    assert str(mdic) == '-P8'

    mdic = pitchtools.NamedIntervalClass('perfect', -8)
    assert str(mdic) == '-P8'

    mdic = pitchtools.NamedIntervalClass('perfect', 8)
    assert str(mdic) == '+P8'

    mdic = pitchtools.NamedIntervalClass('perfect', 15)
    assert str(mdic) == '+P8'


def test_pitchtools_NamedIntervalClass___init___02():
    r'''Unisons and octaves are treated differently.
    '''

    mdic = pitchtools.NamedIntervalClass('perfect', -1)
    assert str(mdic) == 'P1'

    mdic = pitchtools.NamedIntervalClass('perfect', 1)
    assert str(mdic) == 'P1'
