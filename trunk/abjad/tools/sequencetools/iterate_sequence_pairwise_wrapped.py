def iterate_sequence_pairwise_wrapped(sequence):
    '''.. versionadded:: 1.1

    Iterate `sequence` pairwise wrapped::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.iterate_sequence_pairwise_wrapped(range(6)))
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]

    Return pair generator.
    '''

    for i in range(len(sequence)):
        yield (sequence[i], sequence[(i + 1) % len(sequence)])
