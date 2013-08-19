# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval___abs___01():

    interval = pitchtools.NamedHarmonicInterval('minor', 3)
    assert abs(interval) == pitchtools.NamedHarmonicInterval('minor', 3)


def test_NamedHarmonicInterval___abs___02():

    interval = pitchtools.NamedHarmonicInterval('minor', -3)
    assert abs(interval) == pitchtools.NamedHarmonicInterval('minor', 3)
