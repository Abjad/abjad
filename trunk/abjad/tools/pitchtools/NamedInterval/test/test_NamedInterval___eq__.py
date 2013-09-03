# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedInterval___eq___01():

    diatonic_interval_1 = pitchtools.NamedInterval('minor', 2)
    diatonic_interval_2 = pitchtools.NamedInterval('minor', 2)

    assert diatonic_interval_1 == diatonic_interval_2



def test_NamedInterval___eq___02():

    diatonic_interval_1 = pitchtools.NamedInterval('minor', 2)
    diatonic_interval_2 = pitchtools.NamedInterval('augmented', 1)

    assert not diatonic_interval_1 == diatonic_interval_2
