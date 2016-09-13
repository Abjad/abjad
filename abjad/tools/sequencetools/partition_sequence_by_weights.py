# -*- coding: utf-8 -*-
from abjad.tools import mathtools


def partition_sequence_by_weights(
    sequence,
    weights,
    cyclic=False,
    overhang=False,
    allow_part_weights=Exact,
    ):
    r'''Partitions `sequence` by `weights` exactly.

    ::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]

    ..  container:: example

        **Example 1.** Partitions sequence once by weights:
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [3, 9],
            ...     cyclic=False,
            ...     overhang=False,
            ...     )
            [[3], [3, 3, 3]]

    ..  container:: example

        **Example 2.** Partitions sequence once by weights. Allows overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [3, 9],
            ...     cyclic=False,
            ...     overhang=True,
            ...     )
            [[3], [3, 3, 3], [4, 4, 4, 4, 5]]

    ..  container:: example

        **Example 3.** Partitions sequence cyclically by weights:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [12],
            ...     cyclic=True,
            ...     overhang=False,
            ...     )
            [[3, 3, 3, 3], [4, 4, 4]]

    ..  container:: example

        **Example 4.** Partitions sequence cyclically by weights. Allows
        overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [12],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            [[3, 3, 3, 3], [4, 4, 4], [4, 5]]

    ::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]

    ..  container:: example

        **Example 5.** Partitions sequence once by weights. Allows part weights
        to be just less than specified:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=False,
            ...     allow_part_weights=Less,
            ...     )
            [[3, 3, 3], [3]]

    ..  container:: example

        **Example 6.** Partitions sequence once by weights. Allows part weights
        to be just less than specified. Allows overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=True,
            ...     allow_part_weights=Less,
            ...     )
            [[3, 3, 3], [3], [4, 4, 4, 4, 5, 5]]

    ..  container:: example

        **Example 7.** Partitions sequence cyclically by weights. Allows part
        weights to be just less than specified:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [10, 5],
            ...     cyclic=True,
            ...     overhang=False,
            ...     allow_part_weights=Less,
            ...     )
            [[3, 3, 3], [3], [4, 4], [4], [4, 5], [5]]

    ..  container:: example

        **Example 8.** Partitions sequence cyclically by weights. Allows part
        weights to be just less than specified. Allows overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [10, 5],
            ...     cyclic=True,
            ...     overhang=True,
            ...     allow_part_weights=Less,
            ...     )
            [[3, 3, 3], [3], [4, 4], [4], [4, 5], [5]]

    ::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]

    ..  container:: example

        **Example 9.** Partitions sequence once by weights. Allow part weights
        to be just more than specified:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=False,
            ...     allow_part_weights=More,
            ...     )
            [[3, 3, 3, 3], [4]]

    ..  container:: example

        **Example 10.** Partitions sequence once by weights. Allows part
        weights to be just more than specified. Allows overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=True,
            ...     allow_part_weights=More,
            ...     )
            [[3, 3, 3, 3], [4], [4, 4, 4, 5, 5]]

    ..  container:: example

        **Example 11.** Partitions sequence cyclically by weights. Allows part
        weights to be just more than specified:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [10, 4],
            ...     cyclic=True,
            ...     overhang=False,
            ...     allow_part_weights=More,
            ...     )
            [[3, 3, 3, 3], [4], [4, 4, 4], [5]]

    ..  container:: example

        **Example 12.** Partitions sequence cyclically by weights. Allows part
        weights to be just more than specified. Allows overhang:

        ::

            >>> sequencetools.partition_sequence_by_weights(
            ...     sequence,
            ...     [10, 4],
            ...     cyclic=True,
            ...     overhang=True,
            ...     allow_part_weights=More,
            ...     )
            [[3, 3, 3, 3], [4], [4, 4, 4], [5], [5]]

    Returns list of sequence objects.
    '''
    from abjad.tools import sequencetools

    if allow_part_weights == Exact:
        candidate = sequencetools.split_sequence(
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
            raise Exception(message)
    elif allow_part_weights == More:
        if not cyclic:
            return _partition_sequence_once_by_weights_at_least(
                sequence,
                weights,
                overhang=overhang,
                )
        else:
            return _partition_sequence_cyclically_by_weights_at_least(
                sequence,
                weights,
                overhang=overhang,
                )
    elif allow_part_weights == Less:
        if not cyclic:
            return _partition_sequence_once_by_weights_at_most(
                sequence,
                weights,
                overhang=overhang,
                )
        else:
            return _partition_sequence_cyclically_by_weights_at_most(
                sequence,
                weights,
                overhang=overhang,
                )
    else:
        message = 'not an ordinal value constant: {!r}.'
        message = message.format(allow_part_weights)
        raise ValueError(message)


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
                raise Exception(message)
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


def _partition_sequence_once_by_weights_at_most(
    sequence,
    weights,
    overhang=False,
    ):
    l_copy = sequence[:]
    result = []
    current_part = []
    for target_weight in weights:
        while True:
            try:
                x = l_copy.pop(0)
            except IndexError:
                message = 'too few elements in sequence.'
                raise Exception(message)
            current_weight = mathtools.weight(current_part)
            candidate_weight = current_weight + mathtools.weight([x])
            if candidate_weight < target_weight:
                current_part.append(x)
            elif candidate_weight == target_weight:
                current_part.append(x)
                result.append(current_part)
                current_part = []
                break
            elif target_weight < candidate_weight:
                if current_part:
                    result.append(current_part)
                    current_part = []
                    l_copy.insert(0, x)
                    break
                else:
                    message = 'elements in sequence too big.'
                    raise Exception(message)
            else:
                message = 'candidate and target weights must compare.'
                raise ValueError(message)
    if overhang:
        left_over = current_part + l_copy
        if left_over:
            result.append(left_over)
    return result


def _partition_sequence_cyclically_by_weights_at_most(
    sequence,
    weights,
    overhang=False,
    ):
    result = []
    current_part = []
    current_target_weight_index = 0
    current_target_weight = weights[current_target_weight_index]
    l_copy = sequence[:]
    while l_copy:
        current_target_weight = \
            weights[current_target_weight_index % len(weights)]
        x = l_copy.pop(0)
        current_part_weight = mathtools.weight(current_part)
        candidate_part_weight = current_part_weight + mathtools.weight([x])
        if candidate_part_weight < current_target_weight:
            current_part.append(x)
        elif candidate_part_weight == current_target_weight:
            current_part.append(x)
            result.append(current_part)
            current_part = []
            current_target_weight_index += 1
        elif current_target_weight < candidate_part_weight:
            if current_part:
                l_copy.insert(0, x)
                result.append(current_part)
                current_part = []
                current_target_weight_index += 1
            else:
                message = 'elements in sequence too big.'
                raise Exception(message)
        else:
            message = 'candidate and target rates must compare.'
            raise ValueError(message)
    if current_part:
        if overhang:
            result.append(current_part)
    return result