# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval___eq___01():

    diatonic_interval_1 = pitchtools.NamedHarmonicInterval('minor', 2)
    diatonic_interval_2 = pitchtools.NamedHarmonicInterval('minor', 2)

    assert diatonic_interval_1 == diatonic_interval_2


def test_NamedHarmonicInterval___eq___02():

    diatonic_interval_1 = pitchtools.NamedHarmonicInterval('minor', 2)
    diatonic_interval_2 = pitchtools.NamedHarmonicInterval('augmented', 1)

    assert not diatonic_interval_1 == diatonic_interval_2
