# -*- encoding: utf-8 -*-


def increase_elements_cyclically(sequence, addenda):
    '''Increases `sequence` cyclically by `addenda`.

    ::

        >>> sequencetools.increase_elements_cyclically(range(10), [10, -10])
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    Returns list.
    '''

    if not isinstance(sequence, (list, tuple)):
        raise TypeError

    result = []
    for i, element in enumerate(sequence):
        new = element + addenda[i % len(addenda)]
        result.append(new)

    return result
