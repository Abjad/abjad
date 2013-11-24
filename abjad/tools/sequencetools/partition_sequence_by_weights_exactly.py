# -*- encoding: utf-8 -*-


def partition_sequence_by_weights_exactly(
    sequence, 
    weights, 
    cyclic=False, 
    overhang=False,
    ):
    r'''Partition `sequence` by `weights` exactly.

    ::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]

    ..  container:: example

        **Example 1.** Partition sequence once by weights exactly without 
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights_exactly(
            ...     sequence, 
            ...     [3, 9], 
            ...     cyclic=False, 
            ...     overhang=False,
            ...     )
            [[3], [3, 3, 3]]

    ..  container:: example

        **Example 2.** Partition sequence once by weights exactly with 
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights_exactly(
            ...     sequence, 
            ...     [3, 9], 
            ...     cyclic=False, 
            ...     overhang=True,
            ...     )
            [[3], [3, 3, 3], [4, 4, 4, 4, 5]]

    ..  container:: example

        **Example 3.** Partition sequence cyclically by weights exactly 
        without overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights_exactly(
            ...     sequence, 
            ...     [12], 
            ...     cyclic=True, 
            ...     overhang=False,
            ...     )
            [[3, 3, 3, 3], [4, 4, 4]]

    ..  container:: example

        **Example 4.** Partition sequence cyclically by weights exactly with 
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights_exactly(
            ...     sequence, 
            ...     [12], 
            ...     cyclic=True, 
            ...     overhang=True,
            ...     )
            [[3, 3, 3, 3], [4, 4, 4], [4, 5]]

    Returns list sequence objects.
    '''
    from abjad.tools import sequencetools

    candidate = sequencetools.split_sequence_by_weights(
        sequence, 
        weights, 
        cyclic=cyclic, 
        overhang=overhang,
        )
    flattened_candidate = sequencetools.flatten_sequence(candidate)
    if flattened_candidate == sequence[:len(flattened_candidate)]:
        return candidate
    else:
        message = 'can not partition exactly.'
        raise PartitionError(message)
