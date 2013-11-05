# -*- encoding: utf-8 -*-


def iterate_sequence_pairwise_wrapped(sequence):
    '''Iterate `sequence` pairwise wrapped:

    ::

        >>> list(sequencetools.iterate_sequence_pairwise_wrapped(range(6)))
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]

    Returns pair generator.
    '''

    for i in range(len(sequence)):
        yield (sequence[i], sequence[(i + 1) % len(sequence)])
