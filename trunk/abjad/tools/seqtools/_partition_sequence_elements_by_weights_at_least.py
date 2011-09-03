from abjad.tools import mathtools


def _partition_sequence_elements_by_weights_at_least(sequence, weights, cyclic, overhang):
    if not cyclic:
        return _partition_sequence_elements_once_by_weights_at_least(sequence, weights, overhang)
    else:
        return _partition_sequence_elements_cyclically_by_weights_at_least(sequence, weights, overhang)


def _partition_sequence_elements_once_by_weights_at_least(sequence, weights, overhang):

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


def _partition_sequence_elements_cyclically_by_weights_at_least(sequence, weights, overhang):

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
