from abjad.tools import mathtools


def map_sequence_elements_to_canonic_tuples(sequence, decrease_parts_monotonically=True):
    '''.. versionadded:: 1.1

    Partition `sequence` elements into canonic parts that decrease monotonically::

        >>> sequencetools.map_sequence_elements_to_canonic_tuples(
        ...     range(10))
        [(0,), (1,), (2,), (3,), (4,), (4, 1), (6,), (7,), (8,), (8, 1)]

    Partition `sequence` elements into canonic parts that increase monotonically::

        >>> sequencetools.map_sequence_elements_to_canonic_tuples(
        ...     range(10), decrease_parts_monotonically=False)
        [(0,), (1,), (2,), (3,), (4,), (1, 4), (6,), (7,), (8,), (1, 8)]

    Raise type error when `sequence` is not a list.

    Raise value error on noninteger elements in `sequence`.

    Return list of tuples.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    if not all([isinstance(x, (int, long)) for x in sequence]):
        raise ValueError

    result = []

    for x in sequence:
        result.append(mathtools.partition_integer_into_canonic_parts(
            x, decrease_parts_monotonically=decrease_parts_monotonically))

    return result
