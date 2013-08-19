# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicIntervalSegment_melodic_chromatic_interval_class_segment_01():

    mciseg = pitchtools.NumberedMelodicIntervalSegment([2, 2, 13, 2, 2, 14, 1])
    "NumberedMelodicIntervalSegment(+2, +2, +13, +2, +2, +14, +1)"
    mcicseg = mciseg.melodic_chromatic_interval_class_segment

    numbers = [2, 2, 1, 2, 2, 2, 1]
    assert mcicseg == pitchtools.NumberedMelodicIntervalClassSegment(numbers)
