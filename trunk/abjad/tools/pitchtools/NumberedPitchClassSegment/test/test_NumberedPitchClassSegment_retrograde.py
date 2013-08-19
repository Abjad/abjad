# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSegment_retrograde_01():

    pcseg = pitchtools.NumberedPitchClassSegment([0, 6, 10, 4, 9, 2])
    PCSeg = pitchtools.NumberedPitchClassSegment

    assert pcseg.retrograde() == PCSeg([2, 9, 4, 10, 6, 0])
