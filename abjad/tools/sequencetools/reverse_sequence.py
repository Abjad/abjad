# -*- coding: utf-8 -*-
import collections


def reverse_sequence(sequence):
    '''Reverses `sequence`.

    ..  container:: example

        **Example 1.** Reverses tuple:

        ::

            >>> sequencetools.reverse_sequence((1, 2, 3, 4, 5))
            (5, 4, 3, 2, 1)

    ..  container:: example

        **Example 2.** Reverses list:

        ::

            >>> sequencetools.reverse_sequence([1, 2, 3, 4, 5])
            [5, 4, 3, 2, 1]

    Returns new object of `sequence` type.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    result = sequencetools.Sequence(sequence).reverse()
    result = sequence_type(result)
    return result
