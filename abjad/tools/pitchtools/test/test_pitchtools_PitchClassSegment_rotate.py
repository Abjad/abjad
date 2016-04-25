# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_rotate_01():

    pitch_class_segment = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])
    assert pitch_class_segment.rotate(0) == pitchtools.PitchClassSegment(
        [0, 6, 10, 4, 9, 2])


def test_pitchtools_PitchClassSegment_rotate_02():
    r'''Rotate right.
    '''

    pitch_class_segment = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])
    assert pitch_class_segment.rotate(1) == \
        pitchtools.PitchClassSegment([2, 0, 6, 10, 4, 9])
    assert pitch_class_segment.rotate(2) == \
        pitchtools.PitchClassSegment([9, 2, 0, 6, 10, 4])
    assert pitch_class_segment.rotate(3) == \
        pitchtools.PitchClassSegment([4, 9, 2, 0, 6, 10])
    assert pitch_class_segment.rotate(4) == \
        pitchtools.PitchClassSegment([10, 4, 9, 2, 0, 6])
    assert pitch_class_segment.rotate(5) == \
        pitchtools.PitchClassSegment([6, 10, 4, 9, 2, 0])
    assert pitch_class_segment.rotate(6) == \
        pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])


def test_pitchtools_PitchClassSegment_rotate_03():
    r'''Rotate left.
    '''

    pitch_class_segment = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])
    assert pitch_class_segment.rotate(-1) == \
        pitchtools.PitchClassSegment([6, 10, 4, 9, 2, 0])
    assert pitch_class_segment.rotate(-2) == \
        pitchtools.PitchClassSegment([10, 4, 9, 2, 0, 6])
    assert pitch_class_segment.rotate(-3) == \
        pitchtools.PitchClassSegment([4, 9, 2, 0, 6, 10])
    assert pitch_class_segment.rotate(-4) == \
        pitchtools.PitchClassSegment([9, 2, 0, 6, 10, 4])
    assert pitch_class_segment.rotate(-5) == \
        pitchtools.PitchClassSegment([2, 0, 6, 10, 4, 9])
    assert pitch_class_segment.rotate(-6) == \
        pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])


def test_pitchtools_PitchClassSegment_rotate_04():

    pitch_class_segment_1 = pitchtools.PitchClassSegment([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),
        pitchtools.NamedPitchClass('f'),
        pitchtools.NamedPitchClass('g'),])
    pitch_class_segment_2 = pitchtools.PitchClassSegment([
        pitchtools.NamedPitchClass('g'),
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),
        pitchtools.NamedPitchClass('f'),])
    assert pitch_class_segment_1.rotate(1) == pitch_class_segment_2
    assert pitch_class_segment_1.rotate(-4) == pitch_class_segment_2
    assert pitch_class_segment_2.rotate(-1) == pitch_class_segment_1
    assert pitch_class_segment_2.rotate(4) == pitch_class_segment_1
