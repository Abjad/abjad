# -*- encoding: utf-8 -*-
import copy


def permute_sequence(sequence, permutation):
    '''Permutes `sequence`.

    ::

        >>> sequencetools.permute_sequence([10, 11, 12, 13, 14, 15], [5, 4, 0, 1, 2, 3])
        [15, 14, 10, 11, 12, 13]

    Returns new object of `sequence` type.
    '''
    from abjad.tools import sequencetools

    if not sequencetools.Sequence(*permutation).is_permutation() or \
        len(sequence) != len(permutation):
        message = '{!r} must be permutation of length {}.'
        message = message.format(permutation, len(sequence))
        raise TypeError(message)

    result = []
    for index in permutation:
        new_element = copy.copy(sequence[index])
        result.append(new_element)
    if isinstance(sequence, str):
        return ''.join(result)
    else:
        return type(sequence)(result)
