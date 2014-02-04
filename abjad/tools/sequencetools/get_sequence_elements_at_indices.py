# -*- encoding: utf-8 -*-


def get_sequence_elements_at_indices(sequence, indices):
    '''Gets `sequence` elements at `indices`.

    ::

        >>> sequencetools.get_sequence_elements_at_indices('string of text', (2, 3, 10, 12))
        ('r', 'i', 't', 'x')

    Returns newly constructed tuple of references to `sequence` elements.
    '''

    result = []
    for i, element in enumerate(sequence):
        if i in indices:
            result.append(element)
    return tuple(result)
