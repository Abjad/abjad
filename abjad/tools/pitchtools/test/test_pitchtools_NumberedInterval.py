# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval_01():

    i = pitchtools.NumberedInterval(3)

    assert abs(i) == pitchtools.NumberedInterval(3)
    assert -i == pitchtools.NumberedInterval(-3)
    assert int(i) == 3
    assert float(i) == 3.0
