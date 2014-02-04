# -*- encoding: utf-8 -*-


def increase_elements_cyclically(
    sequence, 
    addenda, 
    shield=True,
    ):
    '''Increases `sequence` cyclically by `addenda`.

    ::

        >>> sequencetools.increase_elements_cyclically(
        ...     range(10), [10, -10], shield=False)
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    Increases `sequence` cyclically by addenda and map nonpositive values 
    to ``1``:

    ::

        >>> sequencetools.increase_elements_cyclically(
        ...         range(10), [10, -10], shield=True)
        [10, 1, 12, 1, 14, 1, 16, 1, 18, 1]

    Returns list.
    '''

    if not isinstance(sequence, (list, tuple)):
        raise TypeError

    result = []

    for i, element in enumerate(sequence):
        new = element + addenda[i % len(addenda)]
        if shield and new <= 0:
            new = 1
        result.append(new)

    return result
