# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval___init___01():
    r'''Initialize from positive number.
    '''

    i = pitchtools.NumberedInterval(3)
    assert i.number == 3


def test_pitchtools_NumberedInterval___init___02():
    r'''Initialize from negative number.
    '''

    i = pitchtools.NumberedInterval(-3)
    assert i.number == -3


def test_pitchtools_NumberedInterval___init___03():
    r'''Initialize from other numbered interval.
    '''

    i = pitchtools.NumberedInterval(3)
    j = pitchtools.NumberedInterval(i)
    assert i.number == j.number == 3
    assert i is not j


def test_pitchtools_NumberedInterval___init___04():
    r'''Initialize from named interval.
    '''

    named_interval = pitchtools.NamedInterval('perfect', 4)
    i = pitchtools.NumberedInterval(named_interval)
    assert i.number == 5
