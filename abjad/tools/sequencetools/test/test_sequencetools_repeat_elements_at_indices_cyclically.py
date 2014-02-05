# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_repeat_elements_at_indices_cyclically_01():
    r'''Raw cycle token.
    '''

    sequence_2 = list(sequencetools.repeat_elements_at_indices_cyclically(
        range(10), (5, [1, 2]), 3))
    assert sequence_2 == [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]


def test_sequencetools_repeat_elements_at_indices_cyclically_02():
    r'''Cycle token may be a sieve.
    '''

    sieve = sievetools.Sieve.from_cycle_tokens((5, [1, 2]))
    sequence_2 = list(sequencetools.repeat_elements_at_indices_cyclically(
        range(10), sieve, 3))
    assert sequence_2 == [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]
