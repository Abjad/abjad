# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedInterval_chromatic_interval_number_01():

    assert pitchtools.NumberedInterval(-14).chromatic_interval_number == -14
    assert pitchtools.NumberedInterval(14).chromatic_interval_number == 14
    assert pitchtools.NumberedInterval(-2).chromatic_interval_number == -2
    assert pitchtools.NumberedInterval(2).chromatic_interval_number == 2
