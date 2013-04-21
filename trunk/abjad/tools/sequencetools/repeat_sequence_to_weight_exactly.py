import math
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

    # repeat sequence and find overage
    sequence_weight = mathtools.weight(sequence)
    complete_repetitions = int(math.ceil(float(weight) / float(sequence_weight)))
    result = list(sequence)
    result = complete_repetitions * result
    overage = complete_repetitions * sequence_weight - weight

    # remove overage from result
    for element in reversed(result):
        if 0 < overage:
            element_weight = abs(element)
            candidate_overage = overage - element_weight
            if 0 <= candidate_overage:
                overage = candidate_overage
                result.pop()
            else:
                absolute_amount_to_keep = element_weight - overage
                assert 0 < absolute_amount_to_keep
                signed_amount_to_keep = absolute_amount_to_keep
                signed_amount_to_keep *= mathtools.sign(element)
                result.pop()
                result.append(signed_amount_to_keep)
                break
        else:
            break

    # return result
    return type(sequence)(result)
