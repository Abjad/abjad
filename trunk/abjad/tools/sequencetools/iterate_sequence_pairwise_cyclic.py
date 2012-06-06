def iterate_sequence_pairwise_cyclic(sequence):
    '''.. versionadded:: 1.1

    Iterate `sequence` pairwise cyclic::

        >>> from abjad.tools import sequencetools

    ::

        >>> generator = sequencetools.iterate_sequence_pairwise_cyclic(range(6))

    ::

        >>> generator.next()
        (0, 1)
        >>> generator.next()
        (1, 2)
        >>> generator.next()
        (2, 3)
        >>> generator.next()
        (3, 4)
        >>> generator.next()
        (4, 5)
        >>> generator.next()
        (5, 0)
        >>> generator.next()
        (0, 1)
        >>> generator.next()
        (1, 2)

    Return pair generator.
    '''

    i = 0
    while True:
        yield (sequence[i % len(sequence)], sequence[(i + 1) % len(sequence)])
        i += 1
