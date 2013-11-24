# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def partition_sequence_by_weights_at_least(
    sequence, 
    weights, 
    cyclic=False, 
    overhang=False,
    ):
    r'''Partition `sequence` by `weights` at least.

    ::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    
    ..  container:: example

        **Example 1.** Partition sequence once by weights at least without 
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights_at_least(
            ...     sequence, [10, 4], cyclic=False, overhang=False)
            [[3, 3, 3, 3], [4]]

    ..  container:: example

        **Example 2.** Partition sequence once by weights at least with 
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights_at_least(
            ...     sequence, [10, 4], cyclic=False, overhang=True)
            [[3, 3, 3, 3], [4], [4, 4, 4, 5, 5]]

    ..  container:: example

        **Example 3.** Partition sequence cyclically by weights at least 
        without overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights_at_least(
            ...     sequence, [10, 4], cyclic=True, overhang=False)
            [[3, 3, 3, 3], [4], [4, 4, 4], [5]]

    ..  container:: example

        **Example 4.** Partition sequence cyclically by weights at least with 
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights_at_least(
            ...     sequence, [10, 4], cyclic=True, overhang=True)
            [[3, 3, 3, 3], [4], [4, 4, 4], [5], [5]]

    Returns list of sequence objects.
    '''

    if not cyclic:
        return _partition_sequence_once_by_weights_at_least(
            sequence, weights, overhang=overhang)
    else:
        return _partition_sequence_cyclically_by_weights_at_least(
            sequence, weights, overhang=overhang)


def _partition_sequence_once_by_weights_at_least(
    sequence, 
    weights, 
    overhang=False,
    ):

    result = []
    current_part = []
    l_copy = sequence[:]

    for num_weight, target_weight in enumerate(weights):
        while True:
            try:
                x = l_copy.pop(0)
            except IndexError:
                if num_weight + 1 == len(weights):
                    if current_part:
                        result.append(current_part)
                        break
                message = 'too few elements in sequence.'
                raise PartitionError(message)
            current_part.append(x)
            if target_weight <= mathtools.weight(current_part):
                result.append(current_part)
                current_part = []
                break
    if l_copy:
        if overhang:
            result.append(l_copy)
    return result


def _partition_sequence_cyclically_by_weights_at_least(
    sequence, 
    weights, 
    overhang=False,
    ):

    l_copy = sequence[:]
    result = []
    current_part = []
    target_weight_index = 0
    len_weights = len(weights)

    while l_copy:
        target_weight = weights[target_weight_index % len_weights]
        x = l_copy.pop(0)
        current_part.append(x)
        if target_weight <= mathtools.weight(current_part):
            result.append(current_part)
            current_part = []
            target_weight_index += 1

    assert not l_copy

    if current_part:
        if overhang:
            result.append(current_part)

    return result
