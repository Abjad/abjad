# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_rotate_sequence_01():
    r'''Rotates sequence by distance less than or equal to sequence length.
    '''

    assert sequencetools.rotate_sequence(list(range(10)), -3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert sequencetools.rotate_sequence(list(range(10)), 4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    assert sequencetools.rotate_sequence(list(range(10)), 0) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_sequencetools_rotate_sequence_02():
    r'''Rotates sequence by distance greatern than sequence length.
    '''

    assert sequencetools.rotate_sequence(list(range(10)), -23) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert sequencetools.rotate_sequence(list(range(10)), 24) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]


def test_sequencetools_rotate_sequence_03():
    r'''Returns sequence type.
    '''

    sequence = list(range(10))
    new = sequencetools.rotate_sequence(sequence, -1)
    assert isinstance(new, type(sequence))

    sequence = tuple(range(10))
    new = sequencetools.rotate_sequence(sequence, -1)
    assert isinstance(new, type(sequence))


def test_sequencetools_rotate_sequence_04():
    r'''Rotates named pitch segment.
    '''
    pytest.skip('FIXME')

    named_pitch_segment_1 = pitchtools.PitchSegment("c'' d'' e'' f''")
    named_pitch_segment_2 = sequencetools.rotate_sequence(named_pitch_segment_1, -1)
    named_pitch_segment_3 = pitchtools.PitchSegment("d'' e'' f'' c''")

    assert named_pitch_segment_2 == named_pitch_segment_3
    assert isinstance(named_pitch_segment_1, pitchtools.PitchSegment)
    assert isinstance(named_pitch_segment_2, pitchtools.PitchSegment)
    assert isinstance(named_pitch_segment_3, pitchtools.PitchSegment)
