# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_is_equivalent_under_transposition_01():

    pitch_class_segment_1 = pitchtools.PitchClassSegment(['c', 'e', 'b'])
    pitch_class_segment_2 = pitchtools.PitchClassSegment(['f', 'a', 'e'])
    pitch_class_segment_3 = pitchtools.PitchClassSegment(['f', 'a'])

    assert pitch_class_segment_1.is_equivalent_under_transposition(
        pitch_class_segment_1)
    assert pitch_class_segment_1.is_equivalent_under_transposition(
        pitch_class_segment_2)
    assert not pitch_class_segment_1.is_equivalent_under_transposition(
        pitch_class_segment_3)

    assert pitch_class_segment_2.is_equivalent_under_transposition(
        pitch_class_segment_1)
    assert pitch_class_segment_2.is_equivalent_under_transposition(
        pitch_class_segment_2)
    assert not pitch_class_segment_2.is_equivalent_under_transposition(
        pitch_class_segment_3)

    assert not pitch_class_segment_3.is_equivalent_under_transposition(
        pitch_class_segment_1)
    assert not pitch_class_segment_3.is_equivalent_under_transposition(
        pitch_class_segment_2)
    assert pitch_class_segment_3.is_equivalent_under_transposition(
        pitch_class_segment_3)
