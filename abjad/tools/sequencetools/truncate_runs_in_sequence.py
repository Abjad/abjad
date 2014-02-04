# -*- encoding: utf-8 -*-
import numbers


# TODO: this duplicates sequencetools.remove_duplicate_elemens()
#       sequencetools.remove_duplciate_elements() is a better name.
def truncate_runs_in_sequence(sequence):
    '''Truncates subruns of like elements in `sequence` to length ``1``.

    ::

        >>> sequencetools.truncate_runs_in_sequence([1, 1, 2, 3, 3, 3, 9, 4, 4, 4])
        [1, 2, 3, 9, 4]

    Returns empty list when `sequence` is empty:

    ::

        >>> sequencetools.truncate_runs_in_sequence([])
        []

    Raises type error when `sequence` is not a list.

    Returns new list.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    assert all(isinstance(x, numbers.Number) for x in sequence)

    result = []

    if sequence:
        result.append(sequence[0])
        for element in sequence[1:]:
            if not element == result[-1]:
                result.append(element)

    return result
