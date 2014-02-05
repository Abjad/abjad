# -*- encoding: utf-8 -*-


def iterate_sequence_boustrophedon(sequence, duplicates=False):
    '''Iterates `sequence` first forward and then backward,
    with first and last elements appearing only once.

    ::

        >>> list(sequencetools.iterate_sequence_boustrophedon([1, 2, 3, 4, 5]))
        [1, 2, 3, 4, 5, 4, 3, 2]

    Returns generator.
    '''

    sequence_copy = []
    for x in sequence:
        yield x
        sequence_copy.append(x)
    for x in reversed(sequence_copy[1:-1]):
        yield x
