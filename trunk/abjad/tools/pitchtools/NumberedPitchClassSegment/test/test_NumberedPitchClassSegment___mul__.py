# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSegment___mul___01():

    ncpcs1 = pitchtools.NumberedPitchClassSegment([0, 1, 11, 9])
    ncpsc2 = ncpcs1 * 2

    assert ncpsc2 == pitchtools.NumberedPitchClassSegment([0, 1, 11, 9, 0, 1, 11, 9])
