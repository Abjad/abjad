# -*- encoding: utf-8 -*_


def zip_sequences(sequences, cyclic=False, truncate=True):
    r'''Zips `sequences`.

    ..  container:: example

        Zips two `sequences` cyclically:

        ::

            >>> sequences = [[1, 2, 3], ['a', 'b']]
            >>> sequencetools.zip_sequences(sequences, cyclic=True)
            [(1, 'a'), (2, 'b'), (3, 'a')]

    ..  container:: example

        Zips three `sequences` cyclically:

        ::

            >>> sequences = [[10, 11, 12], [20, 21], [30, 31, 32, 33]]
            >>> sequencetools.zip_sequences(sequences, cyclic=True)
            [(10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33)]

    ..  container:: example

        Zips sequences without truncation:

        ::

            >>> sequences = ([1, 2, 3, 4], [11, 12, 13], [21, 22, 23])
            >>> sequencetools.zip_sequences(sequences, truncate=False)
            [(1, 11, 21), (2, 12, 22), (3, 13, 23), (4,)]

    ..  container:: example

        Zips sequences noncyclically and with truncation.
        Equivalent to built-in ``zip()``:

        ::

            >>> sequences = ([1, 2, 3, 4], [11, 12, 13], [21, 22, 23])
            >>> sequencetools.zip_sequences(sequences)
            [(1, 11, 21), (2, 12, 22), (3, 13, 23)]

    Returns list.
    '''
    
    if cyclic: 
        max_length = max([len(x) for x in sequences])
        result = []
        for i in range(max_length):
            part = []
            for sequence in sequences:
                index = i % len(sequence)
                element = sequence[index]
                part.append(element)
            part = tuple(part)
            result.append(part)
    elif not truncate:
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
    elif truncate:
        result = zip(*sequences)

    return result
