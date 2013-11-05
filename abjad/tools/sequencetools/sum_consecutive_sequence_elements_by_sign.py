# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
import itertools


def sum_consecutive_sequence_elements_by_sign(sequence, sign=(-1, 0, 1)):
    '''Sum consecutive `sequence` elements by `sign`:

    ::

        >>> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ::

        >>> sequencetools.sum_consecutive_sequence_elements_by_sign(sequence)
        [0, -2, 5, -5, 8, -11]

    ::

        >>> sequencetools.sum_consecutive_sequence_elements_by_sign(sequence, sign=[-1])
        [0, 0, -2, 2, 3, -5, 1, 2, 5, -11]

    ::

        >>> sequencetools.sum_consecutive_sequence_elements_by_sign(sequence, sign=[0])
        [0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ::

        >>> sequencetools.sum_consecutive_sequence_elements_by_sign(sequence, sign=[1])
        [0, 0, -1, -1, 5, -5, 8, -5, -6]

    ::

        >>> sequencetools.sum_consecutive_sequence_elements_by_sign(sequence, sign=[-1, 0])
        [0, -2, 2, 3, -5, 1, 2, 5, -11]

    ::

        >>> sequencetools.sum_consecutive_sequence_elements_by_sign(sequence, sign=[-1, 1])
        [0, 0, -2, 5, -5, 8, -11]

    ::

        >>> sequencetools.sum_consecutive_sequence_elements_by_sign(sequence, sign=[0, 1])
        [0, -1, -1, 5, -5, 8, -5, -6]

    ::

        >>> sequencetools.sum_consecutive_sequence_elements_by_sign(sequence, sign=[-1, 0, 1])
        [0, -2, 5, -5, 8, -11]

    When ``-1`` in `sign`, sum consecutive negative elements.

    When ``0`` in `sign`, sum consecutive ``0`` elements.

    When ``1`` in `sign`, sum consecutive positive elements.

    Returns list.
    '''

    result = []

    generator = itertools.groupby(sequence, mathtools.sign)
    for current_sign, group in generator:
        if current_sign in sign:
            result.append(sum(group))
        else:
            for x in group:
                result.append(x)

    return result
