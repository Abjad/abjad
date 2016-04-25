# -*- coding: utf-8 -*-
import collections


def remove_subsequence_of_weight_at_index(sequence, weight, index):
    '''Removes subsequence of `weight` at `index`.

    ..  container:: example

        **Example 1.** Removes subsequence of tuple:

        ::

            >>> sequence = (1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6)
            >>> sequencetools.remove_subsequence_of_weight_at_index(sequence, 13, 4)
            (1, 1, 2, 3, 5, 5, 6)

    ..  container:: example

        **Example 2.** Removes subsequence of list:

        ::

            >>> sequence = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
            >>> sequencetools.remove_subsequence_of_weight_at_index(sequence, 13, 4)
            [1, 1, 2, 3, 5, 5, 6]

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    result = list(sequence[:index])
    total = 0
    for element in sequence[index:]:
        if weight <= total:
            result.append(element)
        elif weight < total + element:
            result.append(total + element - weight)
        total += element
    result = sequence_type(result)
    return result
