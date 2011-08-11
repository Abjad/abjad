def get_sequence_elements_at_indices(sequence, indices):
    '''.. versionadded:: 2.0

    Get `sequence` elements at `indices`::

        abjad> from abjad.tools import seqtools

    ::

        abjad> seqtools.get_sequence_elements_at_indices('string of text', (2, 3, 10, 12))
        ('r', 'i', 't', 'x')

    Return newly constructed tuple of references to `sequence` elements.
    '''

    result = [ ]
    for i, element in enumerate(sequence):
        if i in indices:
            result.append(element)
    return tuple(result)
