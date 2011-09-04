from abjad.tools.mathtools.cumulative_sums_zero import cumulative_sums_zero


def cumulative_sums_zero_pairwise(sequence):
    '''List pairwise cumulative sums of `sequence` from ``0``::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.cumulative_sums_zero_pairwise([1, 2, 3, 4, 5, 6])
        [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]

    Return list of pairs.

    .. versionchanged:: 2.0
        renamed ``sequencetools.pairwise_cumulative_sums_zero()`` to
        ``mathtools.cumulative_sums_zero_pairwise()``.
    '''
    from abjad.tools import sequencetools

    return list(sequencetools.iterate_sequence_pairwise_strict(cumulative_sums_zero(sequence)))
