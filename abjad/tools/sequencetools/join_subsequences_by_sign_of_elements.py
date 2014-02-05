# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def join_subsequences_by_sign_of_elements(sequence):
    '''Join subsequences in `sequence` by sign of elements.

    ::

        >>> sequence = [[1, 2], [3, 4], [-5, -6, -7], [-8, -9, -10], [11, 12]]
        >>> sequencetools.join_subsequences_by_sign_of_elements(sequence)
        [[1, 2, 3, 4], [-5, -6, -7, -8, -9, -10], [11, 12]]

    ::

        >>> sequence = [[1, 2], [], [], [3, 4, 5], [6, 7]]
        >>> sequencetools.join_subsequences_by_sign_of_elements(sequence)
        [[1, 2], [], [3, 4, 5, 6, 7]]

    Returns new list.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    if not all(isinstance(x, list) for x in sequence):
        raise TypeError

    if any(mathtools.get_shared_numeric_sign(x) is None for x in sequence):
        raise ValueError

    result = []

    for sublist in sequence:
        try:
            previous_sublist = result[-1]
            if mathtools.get_shared_numeric_sign(previous_sublist) == \
                mathtools.get_shared_numeric_sign(sublist):
                previous_sublist.extend(sublist)
            else:
                result.append(sublist[:])
        except IndexError:
            result.append(sublist[:])

    return result
