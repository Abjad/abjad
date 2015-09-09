# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_repeat_sequence_01():
    r'''Repeat sequence 3 times.
    '''

    sequence_2 = sequencetools.repeat_sequence(list(range(1, 6)), 3)
    assert sequence_2 == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]


def test_sequencetools_repeat_sequence_02():
    r'''Repeat sequence no times.
    '''

    sequence_2 = sequencetools.repeat_sequence(list(range(1, 6)), 0)
    assert sequence_2 == []
