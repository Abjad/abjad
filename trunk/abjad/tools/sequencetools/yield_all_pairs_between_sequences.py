def yield_all_pairs_between_sequences(l, m):
    '''.. versionadded:: 2.0

    Yield all pairs between sequences `l` and `m`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> for pair in sequencetools.yield_all_pairs_between_sequences([1, 2, 3], [4, 5]):
        ...     pair
        ...
        (1, 4)
        (1, 5)
        (2, 4)
        (2, 5)
        (3, 4)
        (3, 5)

    Return pair generator.
    '''

    for x in l:
        for y in m:
            yield x, y
