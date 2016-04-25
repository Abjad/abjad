# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment___getslice___01():
    r'''Returns new pitch-class segment.
    '''

    pitch_class_tokens = [-2, -1.5, 6, 7, -1.5, 7]
    pitch_class_segment_1 = pitchtools.PitchClassSegment(pitch_class_tokens)
    pitch_class_segment_2 = pitch_class_segment_1[:2]

    assert isinstance(pitch_class_segment_2, pitchtools.PitchClassSegment)
    assert pitch_class_segment_2 == \
        pitchtools.PitchClassSegment(pitch_class_tokens[:2])


def test_pitchtools_PitchClassSegment___getslice___02():
    r'''Returns new pitch-class segment.
    '''

    pitch_class_tokens = [-2, -1.5, 6, 7, -1.5, 7]
    pitch_class_segment_1 = pitchtools.PitchClassSegment(pitch_class_tokens)
    pitch_class_segment_2 = pitch_class_segment_1[-2:]

    assert isinstance(pitch_class_segment_2, pitchtools.PitchClassSegment)
    assert pitch_class_segment_2 == \
        pitchtools.PitchClassSegment(pitch_class_tokens[-2:])
