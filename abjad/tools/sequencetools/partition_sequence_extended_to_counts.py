# -*- encoding: utf-8 -*-
import math


def partition_sequence_extended_to_counts(sequence, counts, overhang=True):
    '''Partitions sequence extended to counts.

    ..  container:: example

        **Example 1.** Partition sequence extended to counts with overhang:

        ::

            >>> sequencetools.partition_sequence_extended_to_counts(
            ...     (1, 2, 3, 4), 
            ...     (6, 6, 6), 
            ...     overhang=True,
            ...     )
            [(1, 2, 3, 4, 1, 2), (3, 4, 1, 2, 3, 4), (1, 2, 3, 4, 1, 2), (3, 4)]

    ..  container:: example

        **Example 2.** Partition sequence extended to coutns without overhang:

        ::

            >>> sequencetools.partition_sequence_extended_to_counts(
            ...     (1, 2, 3, 4), 
            ...     (6, 6, 6), 
            ...     overhang=False,
            ...     )
            [(1, 2, 3, 4, 1, 2), (3, 4, 1, 2, 3, 4), (1, 2, 3, 4, 1, 2)]

    Returns sequence of sequence objects.
    '''
    from abjad.tools import sequencetools

    n = int(math.ceil(float(sum(counts)) / len(sequence)))

    sequence = sequencetools.repeat_sequence_n_times(sequence, n)

    return sequencetools.partition_sequence_by_counts(
        sequence, 
        counts, 
        cyclic=False, 
        overhang=overhang,
        )
