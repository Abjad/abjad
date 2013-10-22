# -*- encoding: utf-8 -*-


def iterate_sequence_nwise_strict(sequence, n):
    '''Iterate elements in `sequence` `n` at a time:

    ::

        >>> for x in sequencetools.iterate_sequence_nwise_strict(range(10), 4):
        ...     x
        ...
        (0, 1, 2, 3)
        (1, 2, 3, 4)
        (2, 3, 4, 5)
        (3, 4, 5, 6)
        (4, 5, 6, 7)
        (5, 6, 7, 8)
        (6, 7, 8, 9)

    Returns generator.
    '''

    element_buffer = []
    for element in sequence:
        element_buffer.append(element)
        if len(element_buffer) == n:
            yield tuple(element_buffer)
            element_buffer.pop(0)
