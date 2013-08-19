# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NumberedPitchClassSegment


def test_NumberedPitchClassSegment___getslice___01():
    r'''Return new numbered chromatic pitch-class segment.
    '''

    cpns = [-2, -1.5, 6, 7, -1.5, 7]
    numbered_chromatic_pitch_class_segment_1 = NumberedPitchClassSegment(cpns)
    numbered_chromatic_pitch_class_segment_2 = numbered_chromatic_pitch_class_segment_1[:2]

    assert isinstance(numbered_chromatic_pitch_class_segment_2, NumberedPitchClassSegment)
    assert numbered_chromatic_pitch_class_segment_2 == NumberedPitchClassSegment(cpns[:2])


def test_NumberedPitchClassSegment___getslice___02():
    r'''Return new numbered chromatic pitch-class segment.
    '''

    cpns = [-2, -1.5, 6, 7, -1.5, 7]
    numbered_chromatic_pitch_class_segment_1 = NumberedPitchClassSegment(cpns)
    numbered_chromatic_pitch_class_segment_2 = numbered_chromatic_pitch_class_segment_1[-2:]

    assert isinstance(numbered_chromatic_pitch_class_segment_2, NumberedPitchClassSegment)
    assert numbered_chromatic_pitch_class_segment_2 == NumberedPitchClassSegment(cpns[-2:])
