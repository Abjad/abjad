# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.tonalanalysistools import RootlessChordClass as RCC


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_01():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),])
    chord_class = RCC.from_interval_class_segment(segment)

    assert chord_class == RCC('diminished', 'triad')


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_02():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('major', 3),])
    chord_class = RCC.from_interval_class_segment(segment)

    assert chord_class == RCC('minor', 'triad')


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_03():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('major', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),])
    chord_class = RCC.from_interval_class_segment(segment)

    assert chord_class == RCC('major', 'triad')
