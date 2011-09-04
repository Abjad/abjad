def iterate_sequence_nwise_wrapped(sequence, n):
    '''.. versionadded:: 2.0

    Iterate elements in `sequence` `n` at a time wrapped to beginning::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.iterate_sequence_nwise_wrapped(range(6), 3))
        [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 0), (5, 0, 1)]

    Return generator.
    '''

    first_n_minus_1 = []
    buffer = []
    for element in sequence:
        buffer.append(element)
        if len(buffer) == n:
            yield tuple(buffer)
            buffer.pop(0)
        if len(first_n_minus_1) < n - 1:
            first_n_minus_1.append(element)
    buffer = buffer + first_n_minus_1
    for x in range(n - 1):
        yield tuple(buffer[x:x+n])
