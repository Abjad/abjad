# -*- encoding: utf-8 -*-
import copy
from abjad.tools import mathtools


def partition_sequence_by_counts(
    sequence,
    counts,
    cyclic=False,
    overhang=False,
    copy_elements=False,
    ):
    r'''Partitions sequence by counts.

    ..  container:: example

        **Example 1a.** Partition sequence once by counts without overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(10)),
            ...     [3],
            ...     cyclic=False,
            ...     overhang=False,
            ...     )
            [[0, 1, 2]]

    ..  container:: example

        **Example 1b.** Partition sequence once by counts without overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(16)),
            ...     [4, 3],
            ...     cyclic=False,
            ...     overhang=False,
            ...     )
            [[0, 1, 2, 3], [4, 5, 6]]

    ..  container:: example

        **Example 2a.** Partition sequence cyclically by counts without
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(10)),
            ...     [3],
            ...     cyclic=True,
            ...     overhang=False,
            ...     )
            [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    ..  container:: example

        **Example 2b.** Partition sequence cyclically by counts without
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

        **Example 3a.** Partition sequence once by counts with overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(10)),
            ...     [3],
            ...     cyclic=False,
            ...     overhang=True,
            ...     )
            [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

    ..  container:: example

        **Example 3b.** Partition sequence once by counts with overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(16)),
            ...     [4, 3],
            ...     cyclic=False,
            ...     overhang=True,
            ...     )
            [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]

    ..  container:: example

        **Example 4a.** Partition sequence cyclically by counts with overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(10)),
            ...     [3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    ..  container:: example

        **Example 4b.** Partition sequence cyclically by counts with overhang:

        ::

            >>> sequencetools.partition_sequence_by_counts(
            ...     list(range(16)),
            ...     [4, 3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]

    Returns list of sequence objects.
    '''
    from abjad.tools import sequencetools

    if not isinstance(counts, (tuple, list)):
        message = 'must be list or tuple: {!r}.'
        message = message.format(counts)
        raise TypeError(message)

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
        result.append(type(sequence)(sequence[start:stop]))

    return result