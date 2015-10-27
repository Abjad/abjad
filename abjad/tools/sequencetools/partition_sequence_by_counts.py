# -*- coding: utf-8 -*-
import collections
import copy
from abjad.tools import mathtools


def partition_sequence_by_counts(
    sequence,
    counts,
    cyclic=False,
    overhang=False,
    ):
    r'''Partitions `sequence` by `counts`.

    ..  container:: example

        **Example 1a.** Partitions sequence once by counts without overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(10)),
            ...     [3],
            ...     cyclic=False,
            ...     overhang=False,
            ...     )
            [[0, 1, 2]]

        **Example 1b.** Partitions sequence once by counts without overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(16)),
            ...     [4, 3],
            ...     cyclic=False,
            ...     overhang=False,
            ...     )
            [[0, 1, 2, 3], [4, 5, 6]]

    ..  container:: example

        **Example 2a.** Partitions sequence cyclically by counts without
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(10)),
            ...     [3],
            ...     cyclic=True,
            ...     overhang=False,
            ...     )
            [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        **Example 2b.** Partitions sequence cyclically by counts without
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(16)),
            ...     [4, 3],
            ...     cyclic=True,
            ...     overhang=False,
            ...     )
            [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13]]

    ..  container:: example

        **Example 3a.** Partitions sequence once by counts with overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(10)),
            ...     [3],
            ...     cyclic=False,
            ...     overhang=True,
            ...     )
            [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

        **Example 3b.** Partitions sequence once by counts with overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(16)),
            ...     [4, 3],
            ...     cyclic=False,
            ...     overhang=True,
            ...     )
            [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]

    ..  container:: example

        **Example 4a.** Partitions sequence cyclically by counts with overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(10)),
            ...     [3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

        **Example 4b.** Partitions sequence cyclically by counts with overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(16)),
            ...     [4, 3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]

    Returns list of objects with type equal to that of `sequence`.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, collections.Sequence):
        message = 'must be sequence: {!r}.'
        message = message.format(sequence)
        raise TypeError(message)
    if not isinstance(counts, collections.Iterable):
        message = 'must be iterable: {!r}.'
        message = message.format(counts)
        raise TypeError(message)

    sequence_type = type(sequence)
    result = []
    if cyclic:
        if overhang:
            counts = sequencetools.repeat_sequence_to_weight(
                counts,
                len(sequence),
                )
        else:
            counts = sequencetools.repeat_sequence_to_weight(
                counts, 
                len(sequence), 
                allow_total=Less,
                )
    elif overhang:
        weight_counts = mathtools.weight(counts)
        len_sequence = len(sequence)
        if weight_counts < len_sequence:
            counts = list(counts)
            counts.append(len(sequence) - weight_counts)
    for start, stop in mathtools.cumulative_sums_pairwise(counts):
        part = sequence_type(sequence[start:stop])
        result.append(part)
    return result