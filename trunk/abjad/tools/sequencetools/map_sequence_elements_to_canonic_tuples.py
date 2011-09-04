from abjad.tools import mathtools


def map_sequence_elements_to_canonic_tuples(sequence, direction = 'big-endian'):
    '''.. versionadded:: 1.1

    Partition `sequence` elements into canonic big-endian parts::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.map_sequence_elements_to_canonic_tuples(range(10))
        [(0,), (1,), (2,), (3,), (4,), (4, 1), (6,), (7,), (8,), (8, 1)]

    Partition `sequence` elements into canonic little-endian parts::

        abjad> sequencetools.map_sequence_elements_to_canonic_tuples(range(10), direction = 'little-endian')
        [(0,), (1,), (2,), (3,), (4,), (1, 4), (6,), (7,), (8,), (1, 8)]

    Raise type error when `sequence` is not a list.

    Raise value error on noninteger elements in `sequence`.

    Return list of tuples.

    .. versionchanged:: 2.0
        renamed ``sequencetools.partition_elements_into_canonic_parts()`` to
        ``sequencetools.map_sequence_elements_to_canonic_tuples()``.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    if not all([isinstance(x, (int, long)) for x in sequence]):
        raise ValueError

    result = []

    for x in sequence:
        result.append(mathtools.partition_integer_into_canonic_parts(x, direction = direction))

    return result
