# -*- encoding: utf-8 -*-
from abjad.tools.sequencetools.flatten_sequence import flatten_sequence
from abjad.tools.sequencetools.zip_sequences_without_truncation \
	import zip_sequences_without_truncation


def interlace_sequences(*sequences):
    '''Interlace `sequences`:

    ::

        >>> k = range(100, 103)
        >>> l = range(200, 201)
        >>> m = range(300, 303)
        >>> n = range(400, 408)
        >>> sequencetools.interlace_sequences(k, l, m, n)
        [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]

    Returns list.
    '''

    zipped_sequences = zip_sequences_without_truncation(*sequences)
    flattened_sequences = flatten_sequence(zipped_sequences, depth=1)

    return flattened_sequences
