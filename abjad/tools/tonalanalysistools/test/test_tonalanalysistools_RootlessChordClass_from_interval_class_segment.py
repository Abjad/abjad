# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_01():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),])
    class_ = tonalanalysistools.RootlessChordClass
    chord_class = class_.from_interval_class_segment(segment)

    assert chord_class == class_('diminished', 'triad')


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_02():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('major', 3),])
    class_ = tonalanalysistools.RootlessChordClass
    chord_class = class_.from_interval_class_segment(segment)

    assert chord_class == class_('minor', 'triad')


def test_tonalanalysistools_RootlessChordClass_from_interval_class_segment_03():

    segment = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('major', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),])
    class_ = tonalanalysistools.RootlessChordClass
    chord_class = class_.from_interval_class_segment(segment)

    assert chord_class == class_('major', 'triad')
