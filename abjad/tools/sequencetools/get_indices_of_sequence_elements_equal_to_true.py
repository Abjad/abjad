# -*- encoding: utf-8 -*-


def get_indices_of_sequence_elements_equal_to_true(sequence):
    '''Get indices of `sequence` elements equal to true:

    ::

        >>> sequence = [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]

    ::

        >>> sequencetools.get_indices_of_sequence_elements_equal_to_true(sequence)
        (3, 4, 5, 9, 10, 11, 12)

    Returns newly constructed tuple of zero or more nonnegative integers.
    '''

    result = []
    for i, x in enumerate(sequence):
        if bool(x):
            result.append(i)
    return tuple(result)
