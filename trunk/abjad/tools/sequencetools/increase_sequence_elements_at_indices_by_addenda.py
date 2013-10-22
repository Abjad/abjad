# -*- encoding: utf-8 -*-


def increase_sequence_elements_at_indices_by_addenda(sequence, addenda, indices):
    '''Increase `sequence` by `addenda` at `indices`:

    ::

        >>> sequence = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]

    ::

        >>> sequencetools.increase_sequence_elements_at_indices_by_addenda(
        ...     sequence, [0.5, 0.5], [0, 4, 8])
        [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

    Returns list.
    '''
    from abjad.tools import sequencetools

    # assert no overlaps
    tmp = sequencetools.flatten_sequence([range(i, len(addenda)) for i in indices])
    assert len(tmp) == len(set(tmp))

    result = sequence[:]

    for i in indices:
        for j in range(len(addenda)):
            result[i+j] += addenda[j]

    return result
