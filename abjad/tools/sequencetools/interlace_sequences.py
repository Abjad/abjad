# -*- coding: utf-8 -*-
import collections


def interlace_sequences(sequences):
    '''Interlaces `sequences`.

    ..  container:: example

        **Example 1.** Interlaces generators:

        ::

            >>> sequences = []
            >>> sequences.append(range(100, 103))
            >>> sequences.append(range(200, 201))
            >>> sequences.append(range(300, 303))
            >>> sequences.append(range(400, 408))
            >>> sequencetools.interlace_sequences(sequences)
            [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]

    ..  container:: example

        **Example 2.** Interlaces tuples:

        ::

            >>> sequences = []
            >>> sequences.append(tuple(range(100, 103)))
            >>> sequences.append(tuple(range(200, 201)))
            >>> sequences.append(tuple(range(300, 303)))
            >>> sequences.append(tuple(range(400, 408)))
            >>> sequencetools.interlace_sequences(sequences)
            [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]

    ..  container:: example

        **Example 3.** Interlaces lists:

        ::

            >>> sequences = []
            >>> sequences.append(list(range(100, 103)))
            >>> sequences.append(list(range(200, 201)))
            >>> sequences.append(list(range(300, 303)))
            >>> sequences.append(list(range(400, 408)))
            >>> sequencetools.interlace_sequences(sequences)
            [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]

    ..  container:: example

        **Example 4.** Interlaces strings:

        ::

            >>> sequences = []
            >>> sequences.append('first')
            >>> sequences.append('second')
            >>> sequencetools.interlace_sequences(sequences)
            ['f', 's', 'i', 'e', 'r', 'c', 's', 'o', 't', 'n', 'd']

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
