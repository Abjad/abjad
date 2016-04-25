# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedIntervalClass___init___01():

    mcic = pitchtools.NumberedIntervalClass(3)

    assert repr(mcic) == 'NumberedIntervalClass(3)'
    assert str(mcic) == '+3'
    assert mcic.number == 3


def test_pitchtools_NumberedIntervalClass___init___02():
    r'''Works with numbers less or equal to -12.
    '''

    mcic = pitchtools.NumberedIntervalClass(-12)
    assert repr(mcic) == 'NumberedIntervalClass(-12)'
    assert str(mcic) == '-12'
    assert mcic.number == -12

    mcic = pitchtools.NumberedIntervalClass(-13)
    assert repr(mcic) == 'NumberedIntervalClass(-1)'
    assert str(mcic) == '-1'
    assert mcic.number == -1


def test_pitchtools_NumberedIntervalClass___init___03():
    r'''Works with numbers greater than 12.
    '''

    mcic = pitchtools.NumberedIntervalClass(12)
    assert repr(mcic) == 'NumberedIntervalClass(12)'
    assert str(mcic) == '+12'
    assert mcic.number == 12

    mcic = pitchtools.NumberedIntervalClass(13)
    assert repr(mcic) == 'NumberedIntervalClass(1)'
    assert str(mcic) == '+1'
    assert mcic.number == 1


def test_pitchtools_NumberedIntervalClass___init___04():
    r'''Works with other interval-class instances.
    '''

    mcic = pitchtools.NumberedIntervalClass(12)
    new_mcic = pitchtools.NumberedIntervalClass(mcic)
    assert repr(mcic) == 'NumberedIntervalClass(12)'
    assert str(mcic) == '+12'
    assert mcic.number == 12
