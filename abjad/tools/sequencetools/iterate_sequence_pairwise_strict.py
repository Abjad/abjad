# -*- encoding: utf-8 -*-


def iterate_sequence_pairwise_strict(sequence):
    '''Iterates `sequence` pairwise strict.

    ::

        >>> list(sequencetools.iterate_sequence_pairwise_strict(range(6)))
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]

    Returns pair generator.
    '''

    previous = None
    for x in sequence:
        current = x
        if previous is not None:
            yield previous, current
        previous = current
