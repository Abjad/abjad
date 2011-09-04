from abjad.tools import mathtools


def map_sequence_elements_to_numbered_sublists(sequence):
    '''.. versionadded:: 1.1

    Map `sequence` elements to numbered sublists::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.map_sequence_elements_to_numbered_sublists([1, 2, -3, -4, 5])
        [[1], [2, 3], [-4, -5, -6], [-7, -8, -9, -10], [11, 12, 13, 14, 15]]

    ::

        abjad> sequencetools.map_sequence_elements_to_numbered_sublists([1, 0, -3, -4, 5])
        [[1], [], [-2, -3, -4], [-5, -6, -7, -8], [9, 10, 11, 12, 13]]

    Note that numbering starts at ``1``.

    Return newly constructed list of lists.

    .. versionchanged:: 2.0
        renamed ``sequencetools.lengths_to_counts()`` to
        ``sequencetools.map_sequence_elements_to_numbered_sublists()``.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    if not all([isinstance(x, (int, long)) for x in sequence]):
        raise ValueError

    result = []
    cur = 1

    for length in sequence:
        abs_length = abs(length)
        part = range(cur, cur + abs_length)
        part = [mathtools.sign(length) * x for x in part]
        result.append(part)
        cur += abs_length

    return result
