def truncate_sequence_to_sum(sequence, target_sum):
    '''.. versionadded:: 1.1

    Truncate `sequence` to `target_sum`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> for n in range(10):
        ...     print n, sequencetools.truncate_sequence_to_sum([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10], n)
        ...
        0 []
        1 [-1, 2]
        2 [-1, 2, -3, 4]
        3 [-1, 2, -3, 4, -5, 6]
        4 [-1, 2, -3, 4, -5, 6, -7, 8]
        5 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        6 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        7 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        8 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        9 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

    Return empty list when `target_sum` is ``0``::

        abjad> sequencetools.truncate_sequence_to_sum([1, 2, 3, 4, 5], 0)
        []

    Raise type error when `sequence` is not a list.

    Raise value error on negative `target_sum`.

    Return new list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.truncate_to_sum()`` to
        ``sequencetools.truncate_sequence_to_sum()``.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    total = target_sum

    if total < 0:
        raise ValueError

    #assert 0 <= total
    result = []

    if total == 0:
        return result

    #kind = type(sequence)
    accumulation = 0
    for e in sequence:
        accumulation += e
        if accumulation < total:
            result.append(e)
        else:
            result.append(total - sum(result))
            break
    #return kind(result)
    return result
