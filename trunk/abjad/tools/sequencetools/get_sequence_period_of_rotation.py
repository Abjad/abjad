from abjad.tools import mathtools
from abjad.tools.sequencetools.get_sequence_degree_of_rotational_symmetry import get_sequence_degree_of_rotational_symmetry


def get_sequence_period_of_rotation(sequence, n):
    '''.. versionadded:: 2.0

    Change `sequence` to period of rotation::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.get_sequence_period_of_rotation([1, 2, 3, 1, 2, 3], 1)
        3

    ::

        abjad> sequencetools.get_sequence_period_of_rotation([1, 2, 3, 1, 2, 3], 2)
        3

    ::

        abjad> sequencetools.get_sequence_period_of_rotation([1, 2, 3, 1, 2, 3], 3)
        1

    Return positive integer.
    '''

    degree = get_sequence_degree_of_rotational_symmetry(sequence)
    period = len(sequence) / degree
    divisors_of_n = set(mathtools.divisors(n))
    divisors_of_period = set(mathtools.divisors(period))
    max_shared_divisor = max(divisors_of_n & divisors_of_period)
    return period / max_shared_divisor
