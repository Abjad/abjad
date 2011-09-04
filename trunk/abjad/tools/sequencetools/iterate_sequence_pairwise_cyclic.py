def iterate_sequence_pairwise_cyclic(sequence):
    '''.. versionadded:: 1.1

    Iterate `sequence` pairwise cyclic::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> generator = sequencetools.iterate_sequence_pairwise_cyclic(range(6))

    ::

        abjad> generator.next()
        (0, 1)
        abjad> generator.next()
        (1, 2)
        abjad> generator.next()
        (2, 3)
        abjad> generator.next()
        (3, 4)
        abjad> generator.next()
        (4, 5)
        abjad> generator.next()
        (5, 0)
        abjad> generator.next()
        (0, 1)
        abjad> generator.next()
        (1, 2)

    Return pair generator.
    '''

    i = 0
    while True:
        yield (sequence[i % len(sequence)], sequence[(i + 1) % len(sequence)])
        i += 1
