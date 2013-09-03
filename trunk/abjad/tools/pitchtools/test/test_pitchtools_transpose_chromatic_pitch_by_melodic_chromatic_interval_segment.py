# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_transpose_chromatic_pitch_by_melodic_chromatic_interval_segment_01():
    mcis = pitchtools.IntervalSegment(
        tokens=[-2, 1, 1, -3, 0],
        item_class=pitchtools.NumberedInterval,
        )
    nucp = pitchtools.NumberedPitch(0)
    result = pitchtools.transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(nucp, mcis)
    assert result == [
        pitchtools.NumberedPitch(-2),
        pitchtools.NumberedPitch(-1),
        pitchtools.NumberedPitch(0),
        pitchtools.NumberedPitch(-3),
        pitchtools.NumberedPitch(-3)
    ]
