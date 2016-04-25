# -*- coding: utf-8 -*-


def cumulative_sums_pairwise(sequence):
    r'''Lists pairwise cumulative sums of `sequence` from ``0``.

    ::

        >>> mathtools.cumulative_sums_pairwise([1, 2, 3, 4, 5, 6])
        [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]

    Returns list of pairs.
    '''
    from abjad.tools import mathtools
    from abjad.tools import sequencetools

    sums = mathtools.cumulative_sums(sequence)
    return list(sequencetools.iterate_sequence_nwise(sums))
