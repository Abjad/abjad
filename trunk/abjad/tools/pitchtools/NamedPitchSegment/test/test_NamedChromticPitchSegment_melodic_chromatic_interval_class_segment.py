# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedChromticPitchSegment_melodic_chromatic_interval_class_segment_01():

    pitch_segment = pitchtools.NamedPitchSegment([-2, -1.5, 6, 7, -1.5, 7])
    result = pitch_segment.melodic_chromatic_interval_class_segment
    #assert result == [0.5, 7.5, 1, -8.5, 8.5]
    assert result == [
        pitchtools.NumberedMelodicIntervalClass(0.5),
        pitchtools.NumberedMelodicIntervalClass(7.5),
        pitchtools.NumberedMelodicIntervalClass(1),
        pitchtools.NumberedMelodicIntervalClass(-8.5),
        pitchtools.NumberedMelodicIntervalClass(8.5)]
