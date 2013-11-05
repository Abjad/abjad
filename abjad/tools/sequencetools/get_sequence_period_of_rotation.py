# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.sequencetools.get_sequence_degree_of_rotational_symmetry import \
    get_sequence_degree_of_rotational_symmetry


def get_sequence_period_of_rotation(sequence, n):
    '''Change `sequence` to period of rotation:

    ::

        >>> sequencetools.get_sequence_period_of_rotation([1, 2, 3, 1, 2, 3], 1)
        3

    ::

        >>> sequencetools.get_sequence_period_of_rotation([1, 2, 3, 1, 2, 3], 2)
        3

    ::

        >>> sequencetools.get_sequence_period_of_rotation([1, 2, 3, 1, 2, 3], 3)
        1

    Returns positive integer.
    '''

    degree = get_sequence_degree_of_rotational_symmetry(sequence)
    period = len(sequence) / degree
    divisors_of_n = set(mathtools.divisors(n))
    divisors_of_period = set(mathtools.divisors(period))
    max_shared_divisor = max(divisors_of_n & divisors_of_period)
    return period / max_shared_divisor
