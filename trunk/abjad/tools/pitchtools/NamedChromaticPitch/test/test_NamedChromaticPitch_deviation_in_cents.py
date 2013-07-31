# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedChromaticPitch_deviation_in_cents_01():
    r'''Deviation defaults to None.
    '''

    p = pitchtools.NamedChromaticPitch('bf', 4)
    assert p.deviation_in_cents is None


def test_NamedChromaticPitch_deviation_in_cents_02():
    r'''Deviation can be int or float.
    '''

    p = pitchtools.NamedChromaticPitch('bf', 4, -31)
    assert p.deviation_in_cents == -31

    p = pitchtools.NamedChromaticPitch('bf', 4, -12.4)
    assert p.deviation_in_cents == -12.4
