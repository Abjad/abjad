# -*- coding: utf-8 -*-
from abjad.tools import mathtools


def partition_sequence_by_ratio_of_lengths(sequence, ratio):
    '''Partitions `sequence` by `ratio` of lengths.

    ..  container:: example

        **Example 1.** Partitions sequence by ``1:1:1`` ratio:

        ::

            >>> sequence = list(range(10))
            >>> sequencetools.partition_sequence_by_ratio_of_lengths(
            ...     sequence,
            ...     [1, 1, 1],
            ...     )
            [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]]

        Returns list of lists.

    ..  container:: example

        **Example 2.** Partitions sequence by ``1:1:2`` ratio:

        ::

            >>> sequence = tuple(range(10))
            >>> sequencetools.partition_sequence_by_ratio_of_lengths(
            ...     sequence,
            ...     [1, 1, 2],
            ...     )
            [(0, 1, 2), (3, 4), (5, 6, 7, 8, 9)]

        Returns list of tuples.

    Uses the rounding magic implemented in
    ``mathtools.partition_integer_by_ratio()`` to avoid fractional part
    lengths.

    Returns list of `sequence` objects.
    '''
    from abjad.tools import sequencetools
    if sequence is None:
        callback = sequencetools.PartitionByRatioOfLengthsCallback(
            ratio=ratio,
            )
        return callback
    ratio = mathtools.Ratio(ratio)
    counts = mathtools.partition_integer_by_ratio(len(sequence), ratio)
    return sequencetools.partition_sequence_by_counts(
        sequence,
        counts,
        cyclic=False,
        overhang=Exact,
        )
