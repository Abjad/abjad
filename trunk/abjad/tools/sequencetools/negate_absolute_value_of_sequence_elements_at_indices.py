def negate_absolute_value_of_sequence_elements_at_indices(sequence, indices):
    '''.. versionadded:: 1.1

    Negate the absolute value of `sequence` elements at `indices`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]

    ::

        abjad> sequencetools.negate_sequence_elements_at_indices(sequence, [0, 1, 2])
        [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    Return newly constructed list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.negate_elements_at_indices_absolutely()`` to
        ``sequencetools.negate_absolute_value_of_sequence_elements_at_indices()``.
    '''

    result = []

    for i, element in enumerate(sequence):
        if (i in indices):
            result.append(-abs(element))
        else:
            result.append(element)

    return result
