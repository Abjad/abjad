# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval_melodic_diatonic_interval_descending_01():

    hdi = pitchtools.NamedHarmonicInterval('major', 2)
    mdi = pitchtools.NamedMelodicInterval('major', -2)
    assert hdi.melodic_diatonic_interval_descending == mdi

    hdi = pitchtools.NamedHarmonicInterval('major', 9)
    mdi = pitchtools.NamedMelodicInterval('major', -9)
    assert hdi.melodic_diatonic_interval_descending == mdi
