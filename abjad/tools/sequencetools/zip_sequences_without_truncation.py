# -*- encoding: utf-8 -*-


def zip_sequences_without_truncation(sequences):
    '''Zips `sequences` without truncation.

    ::

        >>> sequences = ([1, 2, 3, 4], [11, 12, 13], [21, 22, 23])
        >>> sequencetools.zip_sequences_without_truncation(sequences)
        [(1, 11, 21), (2, 12, 22), (3, 13, 23), (4,)]

    Lengths of the tuples returned may differ but will always be
    greater than or equal to ``1``.

    Returns list of tuples.
    '''

    result = []

    max_length = max([len(x) for x in sequences])

    for i in range(max_length):
        part = []
        for sequence in sequences:
            try:
                part.append(sequence[i])
            except IndexError:
                pass
        result.append(tuple(part))

    return result
