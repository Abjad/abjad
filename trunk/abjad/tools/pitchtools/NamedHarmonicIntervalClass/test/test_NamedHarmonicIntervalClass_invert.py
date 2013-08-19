# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicIntervalClass_invert_01():

    hdic = pitchtools.NamedHarmonicIntervalClass('major', 2)
    inversion = pitchtools.NamedHarmonicIntervalClass('minor', 7)
    assert hdic.invert() == inversion

    hdic = pitchtools.NamedHarmonicIntervalClass('minor', 2)
    inversion = pitchtools.NamedHarmonicIntervalClass('major', 7)
    assert hdic.invert() == inversion


def test_NamedHarmonicIntervalClass_invert_02():

    hdic = pitchtools.NamedHarmonicIntervalClass('perfect', 4)
    inversion = pitchtools.NamedHarmonicIntervalClass('perfect', 5)
    assert hdic.invert() == inversion
