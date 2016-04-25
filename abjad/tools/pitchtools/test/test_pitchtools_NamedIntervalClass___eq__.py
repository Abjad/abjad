# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedIntervalClass___eq___01():

    mdic_1 = pitchtools.NamedIntervalClass('perfect', 1)
    mdic_2 = pitchtools.NamedIntervalClass('perfect', -1)

    assert mdic_1 == mdic_2
    assert mdic_2 == mdic_1

    assert not mdic_1 != mdic_2
    assert not mdic_2 != mdic_2

    assert not mdic_1 is mdic_2
    assert not mdic_2 is mdic_1


def test_pitchtools_NamedIntervalClass___eq___02():

    mdic_1 = pitchtools.NamedIntervalClass('perfect', 2)
    mdic_2 = pitchtools.NamedIntervalClass('perfect', 9)

    assert mdic_1 == mdic_2
    assert mdic_2 == mdic_1

    assert not mdic_1 != mdic_2
    assert not mdic_2 != mdic_2

    assert not mdic_1 is mdic_2
    assert not mdic_2 is mdic_1


def test_pitchtools_NamedIntervalClass___eq___03():

    mdic_1 = pitchtools.NamedIntervalClass('perfect', -2)
    mdic_2 = pitchtools.NamedIntervalClass('perfect', -9)

    assert mdic_1 == mdic_2
    assert mdic_2 == mdic_1

    assert not mdic_1 != mdic_2
    assert not mdic_2 != mdic_2

    assert not mdic_1 is mdic_2
    assert not mdic_2 is mdic_1
