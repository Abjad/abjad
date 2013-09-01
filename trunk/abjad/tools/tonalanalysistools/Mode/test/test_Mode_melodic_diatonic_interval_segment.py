# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_Mode_melodic_diatonic_interval_segment_01():

    m2 = pitchtools.NamedMelodicInterval('minor', 2)
    M2 = pitchtools.NamedMelodicInterval('major', 2)

    mdig = tonalanalysistools.Mode('dorian').melodic_diatonic_interval_segment
    intervals = [M2, m2, M2, M2, M2, m2, M2]
    assert mdig == pitchtools.IntervalSegment(intervals)

    mdig = tonalanalysistools.Mode('phrygian').melodic_diatonic_interval_segment
    intervals = [m2, M2, M2, M2, m2, M2, M2]
    assert mdig == pitchtools.IntervalSegment(intervals)

    mdig = tonalanalysistools.Mode('lydian').melodic_diatonic_interval_segment
    intervals = [M2, M2, M2, m2, M2, M2, m2]
    assert mdig == pitchtools.IntervalSegment(intervals)
