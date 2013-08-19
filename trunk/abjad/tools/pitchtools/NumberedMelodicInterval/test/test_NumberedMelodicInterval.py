# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicInterval_01():

    i = pitchtools.NumberedMelodicInterval(3)

    assert abs(i) == pitchtools.NumberedHarmonicInterval(3)
    assert -i == pitchtools.NumberedMelodicInterval(-3)
    assert int(i) == 3
    assert float(i) == 3.0
