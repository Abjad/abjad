def get_indices_of_sequence_elements_equal_to_true(sequence):
    '''.. versionadded:: 1.1

    Get indices of `sequence` elements equal to true::

        >>> from abjad.tools import sequencetools

    ::
        >>> sequence = [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]

    ::

        >>> sequencetools.get_indices_of_sequence_elements_equal_to_true(sequence)
        (3, 4, 5, 9, 10, 11, 12)

    Return newly constructed tuple of zero or more nonnegative integers.

    .. versionchanged:: 2.0
        renamed ``listtools.true_indices()`` to
        ``sequencetools.get_indices_of_sequence_elements_equal_to_true()``.
    '''

    result = []
    for i, x in enumerate(sequence):
        if bool(x):
            result.append(i)
    return tuple(result)
