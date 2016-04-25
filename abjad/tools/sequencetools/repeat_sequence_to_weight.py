# -*- coding: utf-8 -*-
import collections
import math
import numbers
from abjad.tools import mathtools


def repeat_sequence_to_weight(sequence, weight, allow_total=Exact):
    '''Repeats `sequence` to `weight`.

    ..  container:: example

        **Example 1.** Repeats sequence to weight of 23 exactly:

        ::

            >>> sequencetools.repeat_sequence_to_weight((5, -5, -5), 23)
            (5, -5, -5, 5, -3)

        Truncates last element when necessary.

    ..  container:: example

        **Example 2.** Repeats sequence to weight of 23 more:

        ::

            >>> sequencetools.repeat_sequence_to_weight(
            ...     (5, -5, -5),
            ...     23,
            ...     allow_total=More,
            ...     )
            (5, -5, -5, 5, -5)

        Does not truncate last element.

    ..  container:: example

        **Example 3.** Repeats sequence to weight of 23 or less:

        ::

            >>> sequencetools.repeat_sequence_to_weight(
            ...     (5, -5, -5),
            ...     23,
            ...     allow_total=Less,
            ...     )
            (5, -5, -5, 5)

        Discards last element when necessary.

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    # check input
    assert isinstance(weight, numbers.Number), repr(weight)
    assert 0 <= weight

    if allow_total == Exact:
        # repeat sequence and find overage
        sequence_weight = mathtools.weight(sequence)
        complete_repetitions = int(
            math.ceil(float(weight) / float(sequence_weight))
            )
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
    elif allow_total == Less:
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
    elif allow_total == More:
        # initialize result
        result = [sequence[0]]
        # iterate input
        i = 1
        while mathtools.weight(result) < weight:
            result.append(sequence[i % len(sequence)])
            i += 1
        # return result
        return type(sequence)(result)
    else:
        message = 'is not an ordinal value constant: {!r}.'
        message = message.format(allow_total)
        raise ValueError(message)

    # return result
    result = sequence_type(result)
    return result
