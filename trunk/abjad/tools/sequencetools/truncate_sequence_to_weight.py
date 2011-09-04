from abjad.tools import mathtools


def truncate_sequence_to_weight(sequence, weight):
    '''.. versionadded:: 1.1

    Truncate `sequence` to `weight`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> l = [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        abjad> for x in range(10):
        ...     print x, sequencetools.truncate_sequence_to_weight(l, x)
        ...
        0 []
        1 [-1]
        2 [-1, 1]
        3 [-1, 2]
        4 [-1, 2, -1]
        5 [-1, 2, -2]
        6 [-1, 2, -3]
        7 [-1, 2, -3, 1]
        8 [-1, 2, -3, 2]
        9 [-1, 2, -3, 3]

    Return empty list when `weight` is ``0``::

        abjad> sequencetools.truncate_sequence_to_weight([1, 2, 3, 4, 5], 0)
        []

    Raise type error when `sequence` is not a list.

    Raise value error on negative `weight`.

    Return new list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.truncate_to_weight()`` to
        ``sequencetools.truncate_sequence_to_weight()``.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    if weight < 0:
        raise ValueError

    result = []

    if weight == 0:
        return result

    accumulation = 0
    for x in sequence:
        accumulation += abs(x)
        if accumulation < weight:
            result.append(x)
        else:
            sign = mathtools.sign(x)
            trimmed_part = weight - mathtools.weight(result)
            trimmed_part *= sign
            result.append(trimmed_part)
            break

    return result
