import itertools


def partition_sequence_by_value_of_elements(sequence):
    '''.. versionadded:: 1.1

    Group `sequence` elements by equality::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.partition_sequence_by_value_of_elements([0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5])
        [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)]

    Return list of tuples of `sequence` element references.

    .. versionchanged:: 2.0
        renamed ``sequencetools.group_by_equality()`` to
        ``sequencetools.partition_sequence_by_value_of_elements()``.
    '''

    result = []
    g = itertools.groupby(sequence, lambda x: x)
    for n, group in g:
        result.append(tuple(group))
    return result
