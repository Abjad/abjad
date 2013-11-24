# -*- encoding: utf-8 -*-
import copy
from abjad.tools.sequencetools.is_permutation import is_permutation


def permute_sequence(sequence, permutation):
    '''Permute `sequence` by `permutation`:

    ::

        >>> sequencetools.permute_sequence([10, 11, 12, 13, 14, 15], [5, 4, 0, 1, 2, 3])
        [15, 14, 10, 11, 12, 13]

    Returns newly constructed `sequence` object.
    '''

    if not is_permutation(permutation, length=len(sequence)):
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
