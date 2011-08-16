def zip_sequences_without_truncation(*sequences):
    '''.. versionadded:: 1.1.1

    Zip `sequences` nontruncating::

        abjad> from abjad.tools import seqtools

    ::

        abjad> seqtools.zip_sequences_without_truncation([1, 2, 3, 4], [11, 12, 13], [21, 22, 23])
        [(1, 11, 21), (2, 12, 22), (3, 13, 23), (4,)]

    Lengths of the tuples returned may differ but will always be
    greater than or equal to ``1``.

    Return list of tuples.

    .. versionchanged:: 2.0
        renamed ``seqtools.zip_nontruncating( )`` to
        ``seqtools.zip_sequences_without_truncation( )``.
    '''

    result = [ ]

    max_length = max([len(l) for l in sequences])
    for i in range(max_length):
        part = [ ]
        for l in sequences:
            try:
                part.append(l[i])
            except IndexError:
                pass
        result.append(tuple(part))

    return result
