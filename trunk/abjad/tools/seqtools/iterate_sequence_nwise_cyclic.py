def iterate_sequence_nwise_cyclic(sequence, n):
    '''.. versionadded:: 2.0

    Iterate elements in `sequence` cyclically `n` at a time::

        abjad> from abjad.tools import seqtools

    ::

        abjad> g = seqtools.iterate_sequence_nwise_cyclic(range(6), 3)
        abjad> for n in range(10):
        ...   print g.next( )
        (0, 1, 2)
        (1, 2, 3)
        (2, 3, 4)
        (3, 4, 5)
        (4, 5, 0)
        (5, 0, 1)
        (0, 1, 2)
        (1, 2, 3)
        (2, 3, 4)
        (3, 4, 5)

    Return generator.
    '''

    buffer = [ ]
    long_enough = False
    for element in sequence:
        buffer.append(element)
        if not long_enough:
            if n <= len(buffer):
                long_enough = True
        if long_enough:
            yield tuple(buffer[-n:])

    len_sequence = len(buffer)
    cur = len_sequence - n + 1
    while True:
        output = [ ]
        for local_offset in range(n):
            index = (cur + local_offset) % len_sequence
            output.append(buffer[index])
        yield tuple(output)
        cur += 1
        cur %= len_sequence
