from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_reverse_sequence_01():
    '''Reverse sequence.
    '''

    assert sequencetools.reverse_sequence((1, 2, 3, 4, 5)) == (5, 4, 3, 2, 1)
    assert sequencetools.reverse_sequence([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]


def test_sequencetools_reverse_sequence_02():
    '''Reverse sequence.
    '''

    segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
    reversed_segment = pitchtools.NumberedChromaticPitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

    assert sequencetools.reverse_sequence(segment) == reversed_segment


def test_sequencetools_reverse_sequence_03():
    '''Raise exception on nonsequence.
    '''

    assert py.test.raises(TypeError, 'sequencetools.reverse_sequence(17)')
