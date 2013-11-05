# -*- encoding: utf-8 -*-
import itertools
from abjad.tools import mathtools


def partition_sequence_by_sign_of_elements(sequence, sign=(-1, 0, 1)):
    '''Partition `sequence` elements by sign:

    ::

        >>> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ::

        >>> list(sequencetools.partition_sequence_by_sign_of_elements(
        ...     sequence))
        [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    ::

        >>> list(sequencetools.partition_sequence_by_sign_of_elements(
        ...     sequence, sign=[-1]))
        [0, 0, [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

    ::

        >>> list(sequencetools.partition_sequence_by_sign_of_elements(
        ...     sequence, sign=[0]))
        [[0, 0], -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ::

        >>> list(sequencetools.partition_sequence_by_sign_of_elements(
        ...     sequence, sign=[1]))
        [0, 0, -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

    ::

        >>> list(sequencetools.partition_sequence_by_sign_of_elements(
        ...     sequence, sign=[-1, 0]))
        [[0, 0], [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

    ::

        >>> list(sequencetools.partition_sequence_by_sign_of_elements(
        ...     sequence, sign=[-1, 1]))
        [0, 0, [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    ::

        >>> list(sequencetools.partition_sequence_by_sign_of_elements(
        ...     sequence, sign=[0, 1]))
        [[0, 0], -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

    ::

        >>> list(sequencetools.partition_sequence_by_sign_of_elements(
        ...     sequence, sign=[-1, 0, 1]))
        [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    When ``-1`` in ``sign``, group negative elements.

    When ``0`` in ``sign``, group ``0`` elements.

    When ``1`` in ``sign``, group positive elements.

    Returns list of tuples of `sequence` element references.
    '''
    result = []
    g = itertools.groupby(sequence, mathtools.sign)
    for current_sign, group in g:
        if current_sign in sign:
            result.append(type(sequence)(group))
        else:
            for x in group:
                result.append(x)
    return result
