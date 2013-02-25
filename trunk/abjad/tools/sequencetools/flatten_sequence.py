def flatten_sequence(sequence, klasses=None, depth=-1):
    '''.. versionadded:: 1.1

    Flatten `sequence`:

    ::

        >>> sequencetools.flatten_sequence([1, [2, 3, [4]], 5, [6, 7, [8]]])
        [1, 2, 3, 4, 5, 6, 7, 8]

    Flatten `sequence` to depth ``1``:

    ::

        >>> sequencetools.flatten_sequence([1, [2, 3, [4]], 5, [6, 7, [8]]], depth=1)
        [1, 2, 3, [4], 5, 6, 7, [8]]

    Flatten `sequence` to depth ``2``:

    ::

        >>> sequencetools.flatten_sequence([1, [2, 3, [4]], 5, [6, 7, [8]]], depth=2)
        [1, 2, 3, 4, 5, 6, 7, 8]

    Leave `sequence` unchanged.

    Return newly constructed `sequence` object.
    '''

    if klasses is None:
        klasses = (list, tuple)

    assert isinstance(sequence, klasses), repr(sequence)
    sequence_type = type(sequence)
    return sequence_type(_flatten_helper(sequence, klasses, depth))


# Creates an iterator that can generate a flattened list,
# descending down into child elements to a depth given in the
# argments.
# Note: depth < 0 is effectively equivalent to "infinity"
def _flatten_helper(sequence, klasses, depth):
    if not isinstance(sequence, klasses):
        yield sequence
    elif depth == 0:
        for i in sequence:
            yield i
    else:
        for i in sequence:
            # flatten an iterable by one level
            for j in _flatten_helper(i, klasses, depth - 1):
                yield j
