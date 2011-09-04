from abjad.tools import mathtools


def _partition_sequence_elements_by_weights_at_most(sequence, weights, cyclic, overhang):
    if not cyclic:
        return _partition_sequence_elements_once_by_weights_at_most(sequence, weights, overhang)
    else:
        return _partition_sequence_elements_cyclically_by_weights_at_most(sequence, weights, overhang)


def _partition_sequence_elements_once_by_weights_at_most(sequence, weights, overhang):

    l_copy = sequence[:]
    result = []
    cur_part = []

    for target_weight in weights:
        while True:
            try:
                x = l_copy.pop(0)
            except IndexError:
                raise PartitionError('too few elements in sequence.')
            cur_weight = mathtools.weight(cur_part)
            candidate_weight = cur_weight + mathtools.weight([x])
            if candidate_weight < target_weight:
                cur_part.append(x)
            elif candidate_weight == target_weight:
                cur_part.append(x)
                result.append(cur_part)
                cur_part = []
                break
            elif target_weight < candidate_weight:
                if cur_part:
                    result.append(cur_part)
                    cur_part = []
                    l_copy.insert(0, x)
                    break
                else:
                    raise PartitionError('Elements in sequence too big.')
            else:
                raise ValueError('candidate and target weights must compare.')

    if overhang:
        left_over = cur_part + l_copy
        if left_over:
            result.append(left_over)

    return result


def _partition_sequence_elements_cyclically_by_weights_at_most(sequence, weights, overhang):

    result = []
    cur_part = []
    cur_target_weight_index = 0
    cur_target_weight = weights[cur_target_weight_index]
    l_copy = sequence[:]

    while l_copy:
        cur_target_weight = weights[cur_target_weight_index % len(weights)]
        x = l_copy.pop(0)
        cur_part_weight = mathtools.weight(cur_part)
        candidate_part_weight = cur_part_weight + mathtools.weight([x])
        if candidate_part_weight < cur_target_weight:
            cur_part.append(x)
        elif candidate_part_weight == cur_target_weight:
            cur_part.append(x)
            result.append(cur_part)
            cur_part = []
            cur_target_weight_index += 1
        elif cur_target_weight < candidate_part_weight:
            if cur_part:
                l_copy.insert(0, x)
                result.append(cur_part)
                cur_part = []
                cur_target_weight_index += 1
            else:
                raise PartitionError('Elements in sequence too big.')
        else:
            raise ValueError('candidate and target rates must compare.')

    if cur_part:
        if overhang:
            result.append(cur_part)

    return result
