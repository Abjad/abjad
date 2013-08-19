# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedChromticPitchSegment_melodic_diatonic_interval_class_segment_01():

    pitch_segment = pitchtools.NamedPitchSegment([-2, -1, 6, 7, -1, 7])

    #assert pitch_segment.melodic_diatonic_interval_class_segment == [
    #    1, 5, 2, -6, 6]

    assert pitch_segment.melodic_diatonic_interval_class_segment == [
        pitchtools.NamedMelodicIntervalClass('augmented', 1),
        pitchtools.NamedMelodicIntervalClass('perfect', 5),
        pitchtools.NamedMelodicIntervalClass('minor', 2),
        pitchtools.NamedMelodicIntervalClass('minor', -6),
        pitchtools.NamedMelodicIntervalClass('minor', 6)]
