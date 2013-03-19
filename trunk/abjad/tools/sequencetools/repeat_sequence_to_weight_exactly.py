import numbers
from abjad.tools import mathtools


def repeat_sequence_to_weight_exactly(sequence, weight):
    '''.. versionadded:: 1.1

    Repeat `sequence` to `weight` exactly:

    ::

        >>> sequencetools.repeat_sequence_to_weight_exactly((5, -5, -5), 23)
        (5, -5, -5, 5, -3)

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

    # chop overage
    if weight < mathtools.weight(result):
        last_sign = mathtools.sign(result[-1])
        needed_weight = weight - mathtools.weight(result[:-1])
        result = result[:-1] + [last_sign * needed_weight]

    # return result
    return type(sequence)(result)
