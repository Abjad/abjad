# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Mode_named_interval_segment_01():

    m2 = abjad.NamedInterval('minor', 2)
    M2 = abjad.NamedInterval('major', 2)

    mdig = tonalanalysistools.Mode('dorian').named_interval_segment
    intervals = [M2, m2, M2, M2, M2, m2, M2]
    assert mdig == abjad.IntervalSegment(intervals)

    mdig = tonalanalysistools.Mode('phrygian').named_interval_segment
    intervals = [m2, M2, M2, M2, m2, M2, M2]
    assert mdig == abjad.IntervalSegment(intervals)

    mdig = tonalanalysistools.Mode('lydian').named_interval_segment
    intervals = [M2, M2, M2, m2, M2, M2, m2]
    assert mdig == abjad.IntervalSegment(intervals)
