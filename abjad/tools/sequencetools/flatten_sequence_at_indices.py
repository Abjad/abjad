# -*- encoding: utf-8 -*-
from abjad.tools.sequencetools.flatten_sequence import flatten_sequence


def flatten_sequence_at_indices(sequence, indices, classes=None, depth=-1):
    '''Flatten `sequence` at `indices`:

    ::

        >>> sequencetools.flatten_sequence_at_indices([0, 1, [2, 3, 4], [5, 6, 7]], [3])
        [0, 1, [2, 3, 4], 5, 6, 7]

    Flatten `sequence` at negative `indices`:

    ::

        >>> sequencetools.flatten_sequence_at_indices([0, 1, [2, 3, 4], [5, 6, 7]], [-1])
        [0, 1, [2, 3, 4], 5, 6, 7]

    Leave `sequence` unchanged.

    Returns newly constructed `sequence` object.
    '''

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
                flattened = flatten_sequence(element, classes=classes, depth=depth)
                result.extend(flattened)
            except:
                result.append(element)
        else:
            result.append(element)

    result = ltype(result)
    return result
