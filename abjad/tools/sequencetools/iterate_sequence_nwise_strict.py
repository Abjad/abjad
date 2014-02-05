# -*- encoding: utf-8 -*-


def iterate_sequence_nwise_strict(sequence, n=2):
    '''Iterates elements in `sequence` `n` at a time.

    ..  container:: example

        Iterates sequence by quadruples:

        ::

            >>> for x in sequencetools.iterate_sequence_nwise_strict(range(10), n=4):
            ...     x
            ...
            (0, 1, 2, 3)
            (1, 2, 3, 4)
            (2, 3, 4, 5)
            (3, 4, 5, 6)
            (4, 5, 6, 7)
            (5, 6, 7, 8)
            (6, 7, 8, 9)

    ..  container:: example

        Iterates sequence by pairs:

        ::

            >>> for x in sequencetools.iterate_sequence_nwise_strict(range(10), n=2):
            ...     x
            ...
            (0, 1)
            (1, 2)
            (2, 3)
            (3, 4)
            (4, 5)
            (5, 6)
            (6, 7)
            (7, 8)
            (8, 9)

    Returns generator.
    '''

    element_buffer = []
    for element in sequence:
        element_buffer.append(element)
        if len(element_buffer) == n:
            yield tuple(element_buffer)
            element_buffer.pop(0)
