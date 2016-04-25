# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_reverse_sequence_01():
    r'''Reverses sequence.
    '''

    assert sequencetools.reverse_sequence((1, 2, 3, 4, 5)) == (5, 4, 3, 2, 1)
    assert sequencetools.reverse_sequence([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]


def test_sequencetools_reverse_sequence_02():
    r'''Reverses sequence.
    '''

    segment = pitchtools.PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
    reversed_segment = pitchtools.PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

    assert sequencetools.reverse_sequence(segment) == reversed_segment


def test_sequencetools_reverse_sequence_03():
    r'''Raises exception on nonsequence.
    '''

    assert pytest.raises(Exception, 'sequencetools.reverse_sequence(17)')
