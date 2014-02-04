# -*- encoding: utf-8 -*-


def zip_sequences_cyclically(sequences):
    '''Zips `sequences` cyclically.

    ::

        >>> sequences = [[1, 2, 3], ['a', 'b']]
        >>> sequencetools.zip_sequences_cyclically(sequences)
        [(1, 'a'), (2, 'b'), (3, 'a')]

    Arbitrary number of input sequences now allowed.

    ::

        >>> sequences = [[10, 11, 12], [20, 21], [30, 31, 32, 33]]
        >>> sequencetools.zip_sequences_cyclically(sequences)
        [(10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33)]

    Cycles over the elements of the sequences of shorter length.

    Returns list of length equal to sequence of greatest length in `sequences`.
    '''

    # find length of longest sequence
    max_length = max([len(x) for x in sequences])

    # produce list of tuples
    result = []
    for i in range(max_length):
        part = []
        for sequence in sequences:
            index = i % len(sequence)
            element = sequence[index]
            part.append(element)
        part = tuple(part)
        result.append(part)

    # return result
    return result
