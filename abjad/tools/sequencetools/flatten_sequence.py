# -*- encoding: utf-8 -*-
import collections


def flatten_sequence(sequence, classes=None, depth=-1, indices=None):
    '''Flattens `sequence`.

    ..  container:: example

        Flattens sequence completely:

        ::

            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> sequencetools.flatten_sequence(sequence)
            [1, 2, 3, 4, 5, 6, 7, 8]

    ..  container:: example

        Flattens `sequence` to depth ``1``:

        ::

            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> sequencetools.flatten_sequence(sequence, depth=1)
            [1, 2, 3, [4], 5, 6, 7, [8]]

    ..  container:: example

        Flattens `sequence` to depth ``2``:

        ::

            >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
            >>> sequencetools.flatten_sequence(sequence, depth=2)
            [1, 2, 3, 4, 5, 6, 7, 8]

    ..  container:: example

        Flattens `sequence` at `indices`:

        ::

            >>> sequence = [0, 1, [2, 3, 4], [5, 6, 7]]
            >>> sequencetools.flatten_sequence(sequence, indices=[3])
            [0, 1, [2, 3, 4], 5, 6, 7]

    ..  container:: example

        Flattens `sequence` at negative `indices`:

        ::

            >>> sequence = [0, 1, [2, 3, 4], [5, 6, 7]]
            >>> sequencetools.flatten_sequence(sequence, indices=[-1])
            [0, 1, [2, 3, 4], 5, 6, 7]

    Leaves `sequence` unchanged.

    Returns new object of `sequence` type.
    '''
    from abjad.tools import selectiontools

    if classes is None:
        classes = (collections.Sequence, selectiontools.Selection)

    assert isinstance(sequence, classes), repr(sequence)
    sequence_type = type(sequence)

    if indices is None:
        return sequence_type(_flatten_helper(sequence, classes, depth))
    else:
        return sequence_type(
            _flatten_at_indices_helper(sequence, indices, classes, depth)
            )


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

def _flatten_at_indices_helper(sequence, indices, classes, depth):
    from abjad.tools import sequencetools
    if classes is None:
        classes = (list, tuple)
    if not isinstance(sequence, classes):
        raise TypeError()
    ltype = type(sequence)
    len_l = len(sequence)
    indices = [x if 0 <= x else len_l + x for x in indices]
    result = []
    for i, element in enumerate(sequence):
        if i in indices:
            try:
                flattened = sequencetools.flatten_sequence(
                    element,
                    classes=classes,
                    depth=depth,
                    )
                result.extend(flattened)
            except:
                result.append(element)
        else:
            result.append(element)
    result = ltype(result)
    return result