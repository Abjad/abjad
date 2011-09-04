import copy


def rotate_sequence(sequence, n):
    '''.. versionadded:: 1.1

    Rotate `sequence` to the right::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.rotate_sequence(range(10), 4)
        [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

    Rotate `sequence` to the left::

        abjad> sequencetools.rotate_sequence(range(10), -3)
        [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

    Rotate `sequence` neither to the right nor the left::

        abjad> sequencetools.rotate_sequence(range(10), 0)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Return newly created `sequence` object.

    .. versionchanged:: 2.0
        renamed ``sequencetools.rotate()`` to
        ``sequencetools.rotate_sequence()``.
    '''

    result = []
    n = n % len(sequence)

    for element in sequence[-n:len(sequence)] + sequence[:-n]:
        result.append(copy.deepcopy(element))

    return type(sequence)(result)
