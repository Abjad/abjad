# -*- encoding: utf-8 -*-
from abjad import *


def test_Sequence_rotate_01():
    r'''Rotates sequence by distance less than or equal to sequence length.
    '''

    sequence = sequencetools.Sequence(*range(10))
    assert sequence.rotate(-3) == \
        sequencetools.Sequence(3, 4, 5, 6, 7, 8, 9, 0, 1, 2)
    assert sequence.rotate(4) == \
        sequencetools.Sequence(6, 7, 8, 9, 0, 1, 2, 3, 4, 5)
    assert sequence.rotate(0) == \
        sequencetools.Sequence(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)


def test_Sequence_rotate_02():
    r'''Rotates sequence by distance greatern than sequence length.
    '''

    sequence = sequencetools.Sequence(*range(10))
    assert sequence.rotate(-23) == \
        sequencetools.Sequence(3, 4, 5, 6, 7, 8, 9, 0, 1, 2)
    assert sequence.rotate(24) == \
        sequencetools.Sequence(6, 7, 8, 9, 0, 1, 2, 3, 4, 5)


def test_Sequence_rotate_03():
    r'''Returns sequence type.
    '''

    sequence = sequencetools.Sequence(*range(10))
    new = sequence.rotate(-1)
    assert isinstance(new, type(sequence))
    new = sequence.rotate(-1)
    assert isinstance(new, type(sequence))
