# -*- coding: utf-8 -*-
import collections


def permute_sequence(sequence, permutation):
    '''Permutes `sequence`.

    ::

        >>> sequencetools.permute_sequence([10, 11, 12, 13, 14, 15], [5, 4, 0, 1, 2, 3])
        [15, 14, 10, 11, 12, 13]

    Permutes references to `sequence` elements; does not copy `sequence`
    elements.

    Returns new object of `sequence` type.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    if not sequencetools.Sequence(permutation).is_permutation() or \
        len(sequence) != len(permutation):
        message = '{!r} must be permutation of length {}.'
        message = message.format(permutation, len(sequence))
        raise TypeError(message)

    result = []
    for index in permutation:
        new_element = sequence[index]
        result.append(new_element)
    if isinstance(sequence, str):
        result = ''.join(result)

    result = sequence_type(result)
    return result
