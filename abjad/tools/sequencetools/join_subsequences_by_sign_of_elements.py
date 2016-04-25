# -*- coding: utf-8 -*-
import collections
from abjad.tools import mathtools


def join_subsequences_by_sign_of_elements(sequence):
    '''Joins subsequences in `sequence` by sign of elements.

    ..  container:: example

        **Example 1.** Joins lists by sign of elements:

        ::

            >>> sequence = [[1, 2], [3, 4], [-5, -6, -7], [-8, -9, -10], [11, 12]]
            >>> sequencetools.join_subsequences_by_sign_of_elements(sequence)
            [[1, 2, 3, 4], [-5, -6, -7, -8, -9, -10], [11, 12]]

    ..  container:: example

        **Example 2.** Works with empty lists:

        ::

            >>> sequence = [[1, 2], [], [], [3, 4, 5], [6, 7]]
            >>> sequencetools.join_subsequences_by_sign_of_elements(sequence)
            [[1, 2], [], [3, 4, 5, 6, 7]]

    ..  container:: example

        **Example 3.** Joins tuples by sign of elements:

        ::

            >>> sequence = [(1, 2), (), (), (3, 4, 5), (6, 7)]
            >>> sequencetools.join_subsequences_by_sign_of_elements(sequence)
            [(1, 2), (), (3, 4, 5, 6, 7)]

    Returns new list.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must be sequence: {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    if not all(isinstance(x, collections.Sequence) for x in sequence):
        message = 'must contain only sequences: {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    if any(mathtools.get_shared_numeric_sign(x) is None for x in sequence):
        raise ValueError

    sequence_type = type(sequence)

    result = []

    for subsequence in sequence:
        try:
            previous_subsequence = result[-1]
            previous_subsequence_type = type(previous_subsequence)
            previous_sublist = list(previous_subsequence)
            if mathtools.get_shared_numeric_sign(previous_subsequence) == \
                mathtools.get_shared_numeric_sign(subsequence):
                previous_sublist.extend(subsequence)
                previous_subsequence = previous_subsequence_type(
                    previous_sublist)
                result[-1] = previous_subsequence
            else:
                result.append(subsequence[:])
        except IndexError:
            result.append(subsequence[:])

    result = sequence_type(result)

    return result
