# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicIntervalSegment_melodic_chromatic_interval_numbers_01():
    mciseg = pitchtools.NumberedMelodicIntervalSegment([2, 2, 1, 2, 2, 2, 1])

    assert mciseg.melodic_chromatic_interval_numbers == (2, 2, 1, 2, 2, 2, 1)
