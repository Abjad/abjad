# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSegment_invert_01():

    pcseg = pitchtools.NumberedPitchClassSegment([0, 6, 10, 4, 9, 2])

    assert pcseg.invert() == pitchtools.NumberedPitchClassSegment([0, 6, 2, 8, 3, 10])
