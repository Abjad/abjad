# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.tonalanalysistools import ChordQualityIndicator as CQI


def test_ChordQualityIndicator_from_interval_class_segment_01():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),])
    indicator = CQI.from_interval_class_segment(segment)

    assert indicator == CQI('diminished', 'triad')


def test_ChordQualityIndicator_from_interval_class_segment_02():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('major', 3),])
    indicator = CQI.from_interval_class_segment(segment)

    assert indicator == CQI('minor', 'triad')


def test_ChordQualityIndicator_from_interval_class_segment_03():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('major', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),])
    indicator = CQI.from_interval_class_segment(segment)

    assert indicator == CQI('major', 'triad')
