# -*- encoding: utf-8 -*-


def iterate_sequence_nwise_cyclic(sequence, n):
    '''Iterate elements in `sequence` cyclically `n` at a time:

    ::

        >>> g = sequencetools.iterate_sequence_nwise_cyclic(range(6), 3)
        >>> for n in range(10):
        ...   print g.next()
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

    Returns generator.
    '''

    element_buffer = []
    long_enough = False
    for element in sequence:
        element_buffer.append(element)
        if not long_enough:
            if n <= len(element_buffer):
                long_enough = True
        if long_enough:
            yield tuple(element_buffer[-n:])

    len_sequence = len(element_buffer)
    current = len_sequence - n + 1
    while True:
        output = []
        for local_offset in range(n):
            index = (current + local_offset) % len_sequence
            output.append(element_buffer[index])
        yield tuple(output)
        current += 1
        current %= len_sequence
