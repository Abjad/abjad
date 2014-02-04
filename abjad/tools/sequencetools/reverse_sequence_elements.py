# -*- encoding: utf-8 -*-


def reverse_sequence_elements(sequence):
    '''Reverses `sequence` elements.

    ::

        >>> sequencetools.reverse_sequence_elements([1, (2, 3, 4), 5, (6, 7)])
        [1, (4, 3, 2), 5, (7, 6)]

    Returns new `sequence` object.
    '''
    from abjad.tools import sequencetools

    result = []
    for element in sequence:
        try:
            result.append(sequencetools.reverse_sequence(element))
        except TypeError:
            result.append(element)
    result = type(sequence)(result)
    return result
