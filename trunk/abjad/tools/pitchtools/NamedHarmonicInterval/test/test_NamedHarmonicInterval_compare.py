# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval_compare_01():
    r'''Compare on interval numbers when interval numbers differ.
    '''

    hdi_1 = pitchtools.NamedHarmonicInterval('major', 2)
    hdi_2 = pitchtools.NamedHarmonicInterval('major', 3)

    assert not hdi_1 >  hdi_2
    assert not hdi_1 >=  hdi_2
    assert      hdi_1 <  hdi_2
    assert      hdi_1 <= hdi_2


def test_NamedHarmonicInterval_compare_02():
    r'''Compare on semitones numbers when interval numbers are equal.
    '''

    hdi_1 = pitchtools.NamedHarmonicInterval('augmented', 2)
    hdi_2 = pitchtools.NamedHarmonicInterval('minor', 3)

    assert not hdi_1 >  hdi_2
    assert not hdi_1 >=  hdi_2
    assert      hdi_1 <  hdi_2
    assert      hdi_1 <= hdi_2
