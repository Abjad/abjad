# -*- encoding: utf-8 -*-


def flatten_sequence(sequence, classes=None, depth=-1):
    '''Flattens `sequence`.

    ..  container:: example

        Faltten sequence completely:

        ::

            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> sequencetools.flatten_sequence(sequence)
            [1, 2, 3, 4, 5, 6, 7, 8]

    ..  container:: example

        Flatten `sequence` to depth ``1``:

        ::

            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> sequencetools.flatten_sequence(sequence, depth=1)
            [1, 2, 3, [4], 5, 6, 7, [8]]

    ..  container:: example

        Flatten `sequence` to depth ``2``:

        ::

            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> sequencetools.flatten_sequence(sequence, depth=2)
            [1, 2, 3, 4, 5, 6, 7, 8]

    Leaves `sequence` unchanged.

    Returns new object of `sequence` type.
    '''
    from abjad.tools import selectiontools

    if classes is None:
        classes = (list, tuple, selectiontools.Selection)

    assert isinstance(sequence, classes), repr(sequence)
    sequence_type = type(sequence)
    return sequence_type(_flatten_helper(sequence, classes, depth))


# creates an iterator that can generate a flattened list,
# descending down into child elements to a depth given in the arguments.
# note that depth < 0 is effectively equivalent to infinity.
def _flatten_helper(sequence, classes, depth):
    if not isinstance(sequence, classes):
        yield sequence
    elif depth == 0:
        for i in sequence:
            yield i
    else:
        for i in sequence:
            # flatten an iterable by one level
            for j in _flatten_helper(i, classes, depth - 1):
                yield j
