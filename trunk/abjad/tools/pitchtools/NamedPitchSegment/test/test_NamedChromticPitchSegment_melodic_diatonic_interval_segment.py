# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedChromticPitchSegment_melodic_diatonic_interval_segment_01():

    pitch_segment = pitchtools.NamedPitchSegment([-2, -1, 6, 7, -1, 7])

    assert pitch_segment.melodic_diatonic_interval_segment == \
        pitchtools.NamedMelodicIntervalSegment([
        pitchtools.NamedMelodicInterval('augmented', 1),
        pitchtools.NamedMelodicInterval('perfect', 5),
        pitchtools.NamedMelodicInterval('minor', 2),
        pitchtools.NamedMelodicInterval('minor', -6),
        pitchtools.NamedMelodicInterval('minor', 6)])
