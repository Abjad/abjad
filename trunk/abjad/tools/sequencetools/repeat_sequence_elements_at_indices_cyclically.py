# -*- encoding: utf-8 -*-
from abjad.tools import sievetools


def repeat_sequence_elements_at_indices_cyclically(
    sequence, cycle_token, total):
    '''Repeat `sequence` elements at indices specified by `cycle_token` 
    to `total` length:

    ::

        >>> sequencetools.repeat_sequence_elements_at_indices_cyclically(
        ...     range(10), (5, [1, 2]), 3)
        [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

    The `cycle_token` may be a sieve:

    ::

        >>> sieve = sievetools.Sieve.from_cycle_tokens((5, [1, 2]))
        >>> sequencetools.repeat_sequence_elements_at_indices_cyclically(
        ...     range(10), sieve, 3)
        [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

    Returns list.
    '''

    sieve = sievetools.Sieve.from_cycle_tokens(cycle_token)
    list_sequence = list(sequence)
    indices = sieve.get_congruent_bases(len(list_sequence))

    result = []

    for i, element in enumerate(sequence):
        if i in indices:
            result.append(total * [element])
        else:
            result.append(element)

    return result
