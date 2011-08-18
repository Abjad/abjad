def increase_sequence_elements_cyclically_by_addenda(sequence, addenda, shield = True, trim = True):
    '''.. versionadded:: 1.1.

    Increase `sequence` cyclically by `addenda`::

        abjad> from abjad.tools import seqtools

    ::

        abjad> seqtools.increase_sequence_elements_cyclically_by_addenda(range(10), [10, -10], shield = False)
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    Increase `sequence` cyclically by addenda and map nonpositive values to ``1``::

        abjad> seqtools.increase_sequence_elements_cyclically_by_addenda(range(10), [10, -10], shield = True)
        [10, 1, 12, 1, 14, 1, 16, 1, 18, 1]

    Return list.

    .. versionchanged:: 2.0
        renamed ``seqtools.increase_cyclic()`` to
        ``seqtools.increase_sequence_elements_cyclically_by_addenda()``.
    '''

    if not isinstance(sequence, (list, tuple)):
        raise TypeError

    result = [ ]

    for i, element in enumerate(sequence):
        new = element + addenda[i % len(addenda)]
        if shield and new <= 0:
            new = 1
        result.append(new)

    return result
