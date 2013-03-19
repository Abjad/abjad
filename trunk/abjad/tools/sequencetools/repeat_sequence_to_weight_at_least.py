import numbers
from abjad.tools import mathtools


def repeat_sequence_to_weight_at_least(sequence, weight):
    '''.. versionadded:: 1.1

    Repeat `sequence` to `weight` at least:

    ::

        >>> sequencetools.repeat_sequence_to_weight_at_least((5, -5, -5), 23)
        (5, -5, -5, 5, -5)

    Return newly constructed `sequence` object.
    '''

    # check input
    assert isinstance(weight, numbers.Number)
    assert 0 <= weight

    # initialize result
    result = [sequence[0]]

    # iterate input
    i = 1
    while mathtools.weight(result) < weight:
        result.append(sequence[i % len(sequence)])
        i += 1

    # return result
    return type(sequence)(result)
