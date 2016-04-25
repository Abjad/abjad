# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_transpose_01():

    pitch_class_segment_1 = pitchtools.PitchClassSegment([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),
        pitchtools.NamedPitchClass('f'),
        pitchtools.NamedPitchClass('g'),])

    pitch_class_segment_2 = pitchtools.PitchClassSegment([
        pitchtools.NamedPitchClass('df'),
        pitchtools.NamedPitchClass('ef'),
        pitchtools.NamedPitchClass('f'),
        pitchtools.NamedPitchClass('gf'),
        pitchtools.NamedPitchClass('af'),])

    minor_second_ascending = pitchtools.NamedInterval('minor', 2)
    assert pitch_class_segment_1.transpose(minor_second_ascending) == \
        pitch_class_segment_2

    major_seventh_descending = pitchtools.NamedInterval('major', -7)
    assert pitch_class_segment_1.transpose(major_seventh_descending) == \
        pitch_class_segment_2

    minor_second_descending = pitchtools.NamedInterval('minor', -2)
    assert pitch_class_segment_2.transpose(minor_second_descending) == \
        pitch_class_segment_1

    major_seventh_ascending = pitchtools.NamedInterval('major', 7)
    assert pitch_class_segment_2.transpose(major_seventh_ascending) == \
        pitch_class_segment_1


def test_pitchtools_PitchClassSegment_transpose_02():

    pitch_class_segment = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])
    assert pitch_class_segment.transpose(0) == \
        pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])
    assert pitch_class_segment.transpose(1) == \
        pitchtools.PitchClassSegment([1, 7, 11, 5, 10, 3])
    assert pitch_class_segment.transpose(2) == \
        pitchtools.PitchClassSegment([2, 8, 0, 6, 11, 4])
    assert pitch_class_segment.transpose(3) == \
        pitchtools.PitchClassSegment([3, 9, 1, 7, 0, 5])
    assert pitch_class_segment.transpose(4) == \
        pitchtools.PitchClassSegment([4, 10, 2, 8, 1, 6])
    assert pitch_class_segment.transpose(5) == \
        pitchtools.PitchClassSegment([5, 11, 3, 9, 2, 7])
