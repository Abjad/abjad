# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicIntervalClass___init___01():
    r'''Unisons and octaves are treated differently.
    '''

    mdic = pitchtools.NamedMelodicIntervalClass('perfect', -15)
    assert str(mdic) == '-P8'

    mdic = pitchtools.NamedMelodicIntervalClass('perfect', -8)
    assert str(mdic) == '-P8'

    mdic = pitchtools.NamedMelodicIntervalClass('perfect', 8)
    assert str(mdic) == '+P8'

    mdic = pitchtools.NamedMelodicIntervalClass('perfect', 15)
    assert str(mdic) == '+P8'


def test_NamedMelodicIntervalClass___init___02():
    r'''Unisons and octaves are treated differently.
    '''

    mdic = pitchtools.NamedMelodicIntervalClass('perfect', -1)
    assert str(mdic) == 'P1'

    mdic = pitchtools.NamedMelodicIntervalClass('perfect', 1)
    assert str(mdic) == 'P1'
