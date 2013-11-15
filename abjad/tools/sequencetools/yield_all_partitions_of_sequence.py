# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def yield_all_partitions_of_sequence(sequence):
    '''Yields all partitions of `sequence`.

    ::

        >>> sequence = [0, 1, 2, 3]
        >>> result = sequencetools.yield_all_partitions_of_sequence(sequence)
        >>> for partition in result:
        ...     partition
        ...
        [[0, 1, 2, 3]]
        [[0, 1, 2], [3]]
        [[0, 1], [2, 3]]
        [[0, 1], [2], [3]]
        [[0], [1, 2, 3]]
        [[0], [1, 2], [3]]
        [[0], [1], [2, 3]]
        [[0], [1], [2], [3]]

    Returns generator of newly created lists.
    '''

    # TODO: remove type restriction 
    if not isinstance(sequence, list):
        message = '{!r} must be list.'.format(sequence)
        raise TypeError(message)

    partitions = []

    len_l_minus_1 = len(sequence) - 1
    for i in range(2 ** len_l_minus_1):
        binary_string = mathtools.integer_to_binary_string(i)
        binary_string = binary_string.zfill(len_l_minus_1)
        part = sequence[0:1]
        partition = [part]
        for n, token in zip(sequence[1:], binary_string):
            if int(token) == 0:
                part.append(n)
            else:
                part = [n]
                partition.append(part)
        partitions.append(partition)

    return partitions
