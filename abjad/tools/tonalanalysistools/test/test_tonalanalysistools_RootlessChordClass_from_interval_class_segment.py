# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_01():

    segment = abjad.IntervalClassSegment([
        abjad.NamedInversionEquivalentIntervalClass('minor', 3),
        abjad.NamedInversionEquivalentIntervalClass('minor', 3),])
    class_ = tonalanalysistools.RootlessChordClass
    chord_class = class_.from_interval_class_segment(segment)

    assert chord_class == class_('diminished', 'triad')


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_02():

    segment = abjad.IntervalClassSegment([
        abjad.NamedInversionEquivalentIntervalClass('minor', 3),
        abjad.NamedInversionEquivalentIntervalClass('major', 3),])
    class_ = tonalanalysistools.RootlessChordClass
    chord_class = class_.from_interval_class_segment(segment)

    assert chord_class == class_('minor', 'triad')


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_03():

    segment = abjad.IntervalClassSegment([
        abjad.NamedInversionEquivalentIntervalClass('major', 3),
        abjad.NamedInversionEquivalentIntervalClass('minor', 3),])
    class_ = tonalanalysistools.RootlessChordClass
    chord_class = class_.from_interval_class_segment(segment)

    assert chord_class == class_('major', 'triad')
