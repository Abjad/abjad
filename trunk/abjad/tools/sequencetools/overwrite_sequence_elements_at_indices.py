# TODO Implement optional period keyword.
# TODO Read anchor_index and length values cyclically.
def overwrite_sequence_elements_at_indices(sequence, pairs):
    '''.. versionadded:: 1.1

    Overwrite `sequence` elements at indices according to `pairs`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.overwrite_sequence_elements_at_indices(range(10), [(0, 3), (5, 3)])
        [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

    Set `pairs` to a list of ``(anchor_index, length)`` pairs.

    Return new list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.overwrite_slices_at()`` to
        ``sequencetools.overwrite_sequence_elements_at_indices()``.
    '''

    result = sequence[:]

    for anchor_index, length in pairs:
        anchor = result[anchor_index]
        start = anchor_index + 1
        stop = start + length - 1
        for i in range(start, stop):
            try:
                result[i] = anchor
            except IndexError:
                break

    return result
