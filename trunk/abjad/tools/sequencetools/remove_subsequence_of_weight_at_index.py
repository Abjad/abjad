from fractions import Fraction


def remove_subsequence_of_weight_at_index(sequence, weight, index):
    '''.. versionadded:: 1.1

    Remove subsequence of `weight` at `index`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.remove_subsequence_of_weight_at_index((1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6), 13, 4)
        (1, 1, 2, 3, 5, 5, 6)

    Return newly constructed `sequence` object.

    .. versionchanged:: 2.0
        renamed ``listtools.remove_weighted_subrun_at()`` to
        ``sequencetools.remove_subsequence_of_weight_at_index()``.
    '''

    result = list(sequence[:index])
    total = 0
    for element in sequence[index:]:
        if weight <= total:
            result.append(element)
        elif weight < total + element:
            result.append(total + element - weight)
        total += element
    return type(sequence)(result)
