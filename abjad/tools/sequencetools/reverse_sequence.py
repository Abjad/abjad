# -*- encoding: utf-8 -*-


def reverse_sequence(sequence):
    '''Reverses `sequence`.

    ::

        >>> sequencetools.reverse_sequence((1, 2, 3, 4, 5))
        (5, 4, 3, 2, 1)

    Returns new `sequence` object.
    '''

    return type(sequence)(reversed(sequence))
