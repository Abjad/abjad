# -*- coding: utf-8 -*-
import collections
from abjad.tools import mathtools


def truncate_sequence(sequence, sum_=None, weight=None):
    '''Truncates `sequence`.

    ::

        >>> sequence = [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

    ..  container:: example

        **Example 1.** Truncates sequence to weights ranging from 1 to 10:

        ::

            >>> for n in range(1, 11):
            ...     result = sequencetools.truncate_sequence(sequence, weight=n)
            ...     print(n, result)
            ... 
            1 [-1]
            2 [-1, 1]
            3 [-1, 2]
            4 [-1, 2, -1]
            5 [-1, 2, -2]
            6 [-1, 2, -3]
            7 [-1, 2, -3, 1]
            8 [-1, 2, -3, 2]
            9 [-1, 2, -3, 3]
            10 [-1, 2, -3, 4]

    ..  container:: example

        **Example 2.** Truncates sequence to sums ranging from 1 to 10:

        ::

            >>> for n in range(1, 11):
            ...     result = sequencetools.truncate_sequence(sequence, sum_=n)
            ...     print(n, result)
            ... 
            1 [-1, 2]
            2 [-1, 2, -3, 4]
            3 [-1, 2, -3, 4, -5, 6]
            4 [-1, 2, -3, 4, -5, 6, -7, 8]
            5 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
            6 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
            7 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
            8 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
            9 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
            10 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

    ..  container:: example

        **Example 3.** Truncates sequence to zero weight:

        ::

            >>> sequencetools.truncate_sequence(sequence, weight=0)
            []

    ..  container:: example

        **Example 4.** Truncates sequence to zero sum:

        ::

            >>> sequencetools.truncate_sequence(sequence, sum_=0)
            []

    Ignores `sum_` when `weight` and `sum_` are both set.

    Raises type error when `sequence` is not a list.

    Raises value error on negative `sum_`.

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)
    
    sequence_type = type(sequence)

    if weight is not None:
        if weight < 0:
            raise ValueError
        result = []
        if 0 < weight:
            total = 0
            for element in sequence:
                total += abs(element)
                if total < weight:
                    result.append(element)
                else:
                    sign = mathtools.sign(element)
                    trimmed_part = weight - mathtools.weight(result)
                    trimmed_part *= sign
                    result.append(trimmed_part)
                    break
    elif sum_ is not None:
        sum_ = sum_
        if sum_ < 0:
            raise ValueError
        result = []
        if 0 < sum_:
            total = 0
            for element in sequence:
                total += element
                if total < sum_:
                    result.append(element)
                else:
                    result.append(sum_ - sum(result))
                    break

    result = sequence_type(result)
    return result
