import numbers
from abjad.tools import mathtools


def repeat_sequence_to_weight_at_most(sequence, weight):
    '''.. versionadded:: 1.1

    Repeat `sequence` to `weight` at most:

    ::

        >>> sequencetools.repeat_sequence_to_weight_at_most((5, -5, -5), 23)
        (5, -5, -5, 5)

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

    # remove overage
    if weight < mathtools.weight(result):
        result = result[:-1]

    # return result
    return type(sequence)(result)
