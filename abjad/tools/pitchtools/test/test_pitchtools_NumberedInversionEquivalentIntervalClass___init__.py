# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInversionEquivalentIntervalClass___init___01():
    r'''Initialize from zero.
    '''

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(0)
    assert ic.number == 0


def test_pitchtools_NumberedInversionEquivalentIntervalClass___init___02():
    r'''Initialize from positive integer.
    '''

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(1)
    assert ic.number == 1

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(2)
    assert ic.number == 2

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(3)
    assert ic.number == 3

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(4)
    assert ic.number == 4

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(5)
    assert ic.number == 5

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(6)
    assert ic.number == 6


def test_pitchtools_NumberedInversionEquivalentIntervalClass___init___03():
    r'''Initialize from positive float.
    '''

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(0.5)
    assert ic.number == 0.5

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(1.5)
    assert ic.number == 1.5

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(2.5)
    assert ic.number == 2.5

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(3.5)
    assert ic.number == 3.5

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(4.5)
    assert ic.number == 4.5

    ic = pitchtools.NumberedInversionEquivalentIntervalClass(5.5)
    assert ic.number == 5.5
