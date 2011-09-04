def iterate_sequence_pairwise_strict(sequence):
    '''.. versionadded:: 1.1

    Iterate `sequence` pairwise strict::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.iterate_sequence_pairwise_strict(range(6)))
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]

    Return pair generator.
    '''

    prev = None
    for x in sequence:
        cur = x
        if prev is not None:
            yield prev, cur
        prev = cur
