# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedInterval___eq___01():

    named_interval_1 = pitchtools.NamedInterval('minor', 2)
    named_interval_2 = pitchtools.NamedInterval('minor', 2)

    assert named_interval_1 == named_interval_2



def test_NamedInterval___eq___02():

    named_interval_1 = pitchtools.NamedInterval('minor', 2)
    named_interval_2 = pitchtools.NamedInterval('augmented', 1)

    assert not named_interval_1 == named_interval_2
