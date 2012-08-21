from abjad.tools import mathtools


def partition_sequence_by_weights_at_least(sequence, weights, cyclic=False, overhang=False):
    r'''.. versionadded:: 1.1

    Partition `sequence` by `weights` at least. ::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]

    Example 1. Partition sequence once by weights at least without overhang::

        >>> sequencetools.partition_sequence_by_weights_at_least(
        ...     sequence, [10, 4], cyclic=False, overhang=False)
        [[3, 3, 3, 3], [4]]

    Example 2. Partition sequence once by weights at least with overhang::

        >>> sequencetools.partition_sequence_by_weights_at_least(
        ...     sequence, [10, 4], cyclic=False, overhang=True)
        [[3, 3, 3, 3], [4], [4, 4, 4, 5, 5]]

    Example 3. Partition sequence cyclically by weights at least without overhang::

        >>> sequencetools.partition_sequence_by_weights_at_least(
        ...     sequence, [10, 4], cyclic=True, overhang=False)
        [[3, 3, 3, 3], [4], [4, 4, 4], [5]]

    Example 4. Partition sequence cyclically by weights at least with overhang::

        >>> sequencetools.partition_sequence_by_weights_at_least(
        ...     sequence, [10, 4], cyclic=True, overhang=True)
        [[3, 3, 3, 3], [4], [4, 4, 4], [5], [5]]

    Return list of sequence objects.
    '''

    if not cyclic:
        return _partition_sequence_once_by_weights_at_least(sequence, weights, overhang=overhang)
    else:
        return _partition_sequence_cyclically_by_weights_at_least(sequence, weights, overhang=overhang)


def _partition_sequence_once_by_weights_at_least(sequence, weights, overhang=False):

    result = []
    cur_part = []
    l_copy = sequence[:]

    for num_weight, target_weight in enumerate(weights):
        while True:
            try:
                x = l_copy.pop(0)
            except IndexError:
                if num_weight + 1 == len(weights):
                    if cur_part:
                        result.append(cur_part)
                        break
                raise PartitionError('too few elements in sequence.')
            cur_part.append(x)
            if target_weight <= mathtools.weight(cur_part):
                result.append(cur_part)
                cur_part = []
                break
    if l_copy:
        if overhang:
            result.append(l_copy)
    return result


def _partition_sequence_cyclically_by_weights_at_least(sequence, weights, overhang=False):

    l_copy = sequence[:]
    result = []
    cur_part = []
    target_weight_index = 0
    len_weights = len(weights)

    while l_copy:
        target_weight = weights[target_weight_index % len_weights]
        x = l_copy.pop(0)
        cur_part.append(x)
        if target_weight <= mathtools.weight(cur_part):
            result.append(cur_part)
            cur_part = []
            target_weight_index += 1

    assert not l_copy

    if cur_part:
        if overhang:
            result.append(cur_part)

    return result
