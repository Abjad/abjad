import math
from abjad.tools import mathtools


def split_sequence_extended_to_weights(sequence, weights, overhang=True):
    '''.. versionadded:: 2.0

    Split sequence extended to weights.

    Example 1. Split sequence extended to weights with overhang::

        >>> sequencetools.split_sequence_extended_to_weights(
        ...     [1, 2, 3, 4, 5], [7, 7, 7], overhang=True)
        [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3], [4, 5]]

    Example 2. Split sequence extended to weights without overhang::
    
        >>> sequencetools.split_sequence_extended_to_weights(
        ...     [1, 2, 3, 4, 5], [7, 7, 7], overhang=False)
        [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3]]

    Return sequence of sequence objects.
    '''
    from abjad.tools import sequencetools

    n = int(math.ceil(float(mathtools.weight(weights)) / mathtools.weight(sequence)))

    sequence = sequencetools.repeat_sequence_n_times(sequence, n)

    return sequencetools.split_sequence_by_weights(sequence, weights, cyclic=False, overhang=overhang)
