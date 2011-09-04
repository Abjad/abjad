def flatten_sequence(sequence, klasses = None, depth = -1):
    '''.. versionadded:: 1.1

    Flatten `sequence`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.flatten_sequence([1, [2, 3, [4]], 5, [6, 7, [8]]])
        [1, 2, 3, 4, 5, 6, 7, 8]

    Flatten `sequence` to depth ``1``::

        abjad> sequencetools.flatten_sequence([1, [2, 3, [4]], 5, [6, 7, [8]]], depth = 1)
        [1, 2, 3, [4], 5, 6, 7, [8]]

    Flatten `sequence` to depth ``2``::

        abjad> sequencetools.flatten_sequence([1, [2, 3, [4]], 5, [6, 7, [8]]], depth = 2)
        [1, 2, 3, 4, 5, 6, 7, 8]

    Leave `sequence` unchanged.

    Return newly constructed `sequence` object.

    .. versionchanged:: 2.0
        renamed ``listtools.flatten()`` to
        ``sequencetools.flatten_sequence()``.
    '''

    # based on procedure by Mike C. Fletcher
    if klasses is None:
        klasses = (list, tuple)

    assert isinstance(sequence, klasses)
    ltype = type(sequence)
    return ltype(_flatten_helper(sequence, klasses, depth))


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
            # Flatten an iterable by one level
            for j in _flatten_helper(i, klasses, depth - 1):
                yield j
