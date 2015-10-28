# -*- coding: utf-8 -*-
import collections


def interlace_sequences(sequences):
    '''Interlaces `sequences`.

    ..  container:: example

        **Example 1.** Interlaces generators:

        ::

            >>> k = range(100, 103)
            >>> l = range(200, 201)
            >>> m = range(300, 303)
            >>> n = range(400, 408)
            >>> sequencetools.interlace_sequences([k, l, m, n])
            [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]

    Returns list.
    '''
    from abjad.tools import sequencetools

    for sequence in sequences:
        if not isinstance(sequence, collections.Iterable):
            message = 'must be iterable: {!r}.'
            message = message.format(sequence)
            raise Exception(message)

    result = sequencetools.zip_sequences(sequences, truncate=False)
    result = sequencetools.flatten_sequence(result, depth=1)

    assert isinstance(result, list), repr(result)
    return result