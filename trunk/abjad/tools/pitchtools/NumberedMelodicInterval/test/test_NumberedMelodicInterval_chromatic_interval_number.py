# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicInterval_chromatic_interval_number_01():

    assert pitchtools.NumberedMelodicInterval(-14).chromatic_interval_number == -14
    assert pitchtools.NumberedMelodicInterval(14).chromatic_interval_number == 14
    assert pitchtools.NumberedMelodicInterval(-2).chromatic_interval_number == -2
    assert pitchtools.NumberedMelodicInterval(2).chromatic_interval_number == 2
