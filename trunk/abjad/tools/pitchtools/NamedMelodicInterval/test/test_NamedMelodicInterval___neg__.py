# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval___neg___01():

    interval = pitchtools.NamedMelodicInterval('minor', 3)
    assert -interval == pitchtools.NamedMelodicInterval('minor', -3)


def test_NamedMelodicInterval___neg___02():

    interval = pitchtools.NamedMelodicInterval('minor', -3)
    assert -interval == pitchtools.NamedMelodicInterval('minor', 3)
