def iterate_sequence_nwise_strict(sequence, n):
    '''.. versionadded:: 2.0

    Iterate elements in `sequence` `n` at a time::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.iterate_sequence_nwise_strict(range(10), 4))
        [(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (4, 5, 6, 7), (5, 6, 7, 8), (6, 7, 8, 9)]

    Return generator.
    '''

    element_buffer = []
    for element in sequence:
        element_buffer.append(element)
        if len(element_buffer) == n:
            yield tuple(element_buffer)
            element_buffer.pop(0)
