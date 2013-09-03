# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedInterval___init___01():
    r'''Init from positive number.
    '''

    i = pitchtools.NumberedInterval(3)
    assert i.number == 3


def test_NumberedInterval___init___02():
    r'''Init from negative number.
    '''

    i = pitchtools.NumberedInterval(-3)
    assert i.number == -3


def test_NumberedInterval___init___03():
    r'''Init from other chromatic interval.
    '''

    i = pitchtools.NumberedInterval(3)
    j = pitchtools.NumberedInterval(i)
    assert i.number == j.number == 3
    assert i is not j


def test_NumberedInterval___init___04():
    r'''Init from melodic diatonic interval.
    '''

    diatonic_interval = pitchtools.NamedInterval('perfect', 4)
    i = pitchtools.NumberedInterval(diatonic_interval)
    assert i.number == 5
