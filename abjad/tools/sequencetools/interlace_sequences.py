# -*- encoding: utf-8 -*-


def interlace_sequences(*sequences):
    '''Interlaces `sequences`.

    ::

        >>> k = range(100, 103)
        >>> l = range(200, 201)
        >>> m = range(300, 303)
        >>> n = range(400, 408)
        >>> sequencetools.interlace_sequences(k, l, m, n)
        [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]

    Returns list.
    '''
    from abjad.tools import sequencetools

    result = sequencetools.zip_sequences_without_truncation(sequences)
    result = sequencetools.flatten_sequence(result, depth=1)

    return result
