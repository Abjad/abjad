# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedInterval___neg___01():

    interval = pitchtools.NamedInterval('minor', 3)
    assert -interval == pitchtools.NamedInterval('minor', -3)


def test_NamedInterval___neg___02():

    interval = pitchtools.NamedInterval('minor', -3)
    assert -interval == pitchtools.NamedInterval('minor', 3)
