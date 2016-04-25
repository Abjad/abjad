# -*- coding: utf-8 -*-
import collections


def remove_repeated_elements(sequence):
    r'''Removes repeated elements from `sequence`.

    ..  container:: example

        **Example 1.** Removes repeated elements from tuple:

        ::

            >>> sequence = (17, 18, 18, 18, 19, 20, 21, 22, 22, 24, 24)
            >>> sequencetools.remove_repeated_elements(sequence)
            (17, 18, 19, 20, 21, 22, 24)

    ..  container:: example

        **Example 2.** Removes repeated elementsfrom list:

        ::

            >>> sequence = [31, 31, 35, 35, 31, 31, 31, 31, 35]
            >>> sequencetools.remove_repeated_elements(sequence)
            [31, 35, 31, 35]

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    if not sequence:
        return sequence_type()

    result = [sequence[0]]
    for element in sequence[1:]:
        if element != result[-1]:
            result.append(element)

    result = sequence_type(result)
    return result
