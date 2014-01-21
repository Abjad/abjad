# -*- encoding: utf-8 -*-
import copy


def rotate_sequence(sequence, n):
    '''Rotate `sequence` to the right:

    ::

        >>> sequencetools.rotate_sequence(range(10), 4)
        [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

    Rotate `sequence` to the left:

    ::

        >>> sequencetools.rotate_sequence(range(10), -3)
        [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

    Rotate `sequence` neither to the right nor the left:

    ::

        >>> sequencetools.rotate_sequence(range(10), 0)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Returns newly created `sequence` object.
    '''

    result = []
    if len(sequence):
        n = n % len(sequence)
        for element in sequence[-n:len(sequence)] + sequence[:-n]:
            result.append(copy.deepcopy(element))
    return type(sequence)(result)
