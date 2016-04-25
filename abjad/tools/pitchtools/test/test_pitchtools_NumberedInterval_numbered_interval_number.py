# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval_numbered_interval_number_01():

    assert pitchtools.NumberedInterval(-14).numbered_interval_number == -14
    assert pitchtools.NumberedInterval(14).numbered_interval_number == 14
    assert pitchtools.NumberedInterval(-2).numbered_interval_number == -2
    assert pitchtools.NumberedInterval(2).numbered_interval_number == 2
