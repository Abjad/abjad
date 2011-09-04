from abjad.tools import mathtools
import itertools


def partition_sequence_by_sign_of_elements(sequence, sign = [-1, 0, 1]):
    '''.. versionadded:: 1.1

    Partition `sequence` elements by sign::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ::

        abjad> list(sequencetools.partition_sequence_by_sign_of_elements(sequence))
        [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    ::

        abjad> list(sequencetools.partition_sequence_by_sign_of_elements(sequence, sign = [-1]))
        [0, 0, [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

    ::

        abjad> list(sequencetools.partition_sequence_by_sign_of_elements(sequence, sign = [0]))
        [[0, 0], -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ::

        abjad> list(sequencetools.partition_sequence_by_sign_of_elements(sequence, sign = [1]))
        [0, 0, -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

    ::

        abjad> list(sequencetools.partition_sequence_by_sign_of_elements(sequence, sign = [-1, 0]))
        [[0, 0], [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

    ::

        abjad> list(sequencetools.partition_sequence_by_sign_of_elements(sequence, sign = [-1, 1]))
        [0, 0, [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    ::

        abjad> list(sequencetools.partition_sequence_by_sign_of_elements(sequence, sign = [0, 1]))
        [[0, 0], -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

    ::

        abjad> list(sequencetools.partition_sequence_by_sign_of_elements(sequence, sign = [-1, 0, 1]))
        [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    When ``-1`` in ``sign``, group negative elements.

    When ``0`` in ``sign``, group ``0`` elements.

    When ``1`` in ``sign``, group positive elements.

    Return list of tuples of `sequence` element references.

    .. versionchanged:: 2.0
        renamed ``listtools.group_by_sign()`` to
        ``sequencetools.partition_sequence_by_sign_of_elements()``.
    '''

    result = []
    g = itertools.groupby(sequence, mathtools.sign)
    for cur_sign, group in g:
        if cur_sign in sign:
            #result.append(tuple(group))
            result.append(type(sequence)(group))
        else:
            for x in group:
                result.append(x)
    return result
