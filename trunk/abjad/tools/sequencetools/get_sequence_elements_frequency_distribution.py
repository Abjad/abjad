def get_sequence_elements_frequency_distribution(sequence):
    '''.. versionadded:: 2.0

    Get `sequence` elements frequency distribution::

        >>> sequence = [1, 3, 3, 3, 2, 1, 1, 2, 3, 3, 1, 2]

    ::

        >>> sequencetools.get_sequence_elements_frequency_distribution(sequence)
        [(1, 4), (2, 3), (3, 5)]

    Return list of element / count pairs.
    '''
    from abjad.tools import sequencetools

    result = sorted(sequence)
    result = sequencetools.partition_sequence_by_value_of_elements(result)
    result = [(x[0], len(x)) for x in result]
    return result
