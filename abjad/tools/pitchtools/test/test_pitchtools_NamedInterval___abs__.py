# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval___abs___01():

    interval = pitchtools.NamedInterval('minor', 3)
    assert abs(interval) == pitchtools.NamedInterval('minor', 3)


def test_pitchtools_NamedInterval___abs___02():

    interval = pitchtools.NamedInterval('minor', -3)
    assert abs(interval) == pitchtools.NamedInterval('minor', 3)
