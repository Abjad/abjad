# -*- encoding: utf-8 -*-


def iterate_sequence_boustrophedon(sequence, duplicates=False):
    '''Iterates `sequence` boustrophedon.

    ..  container:: example

        Iterates `sequence` first forward and then backward.
        Duplicates neither first nor last elements:

        ::

            >>> sequence = [1, 2, 3, 4, 5]
            >>> generator = sequencetools.iterate_sequence_boustrophedon(
            ...     sequence, duplicates=False)
            >>> list(generator)
            [1, 2, 3, 4, 5, 4, 3, 2]

    ..  container:: example

        Iterates `sequence` first forward and then backward.
        Duplicates both first and last elements:

        ::

            >>> sequence = [1, 2, 3, 4, 5]
            >>> generator = sequencetools.iterate_sequence_boustrophedon(
            ...     sequence, duplicates=True)
            >>> list(generator)
            [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]

    Returns generator.
    '''

    if duplicates:
        sequence_copy = []
        for x in sequence:
            yield x
            sequence_copy.append(x)
        for x in reversed(sequence_copy):
            yield x
    else:
        sequence_copy = []
        for x in sequence:
            yield x
            sequence_copy.append(x)
        for x in reversed(sequence_copy[1:-1]):
            yield x
