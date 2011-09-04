from abjad.tools import mathtools


def yield_all_restricted_growth_functions_of_length(length):
    '''.. versionadded:: 2.0

    Generate all restricted growth functions of `length` in lex order::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> for rgf in sequencetools.yield_all_restricted_growth_functions_of_length(4):
        ...     rgf
        ...
        (1, 1, 1, 1)
        (1, 1, 1, 2)
        (1, 1, 2, 1)
        (1, 1, 2, 2)
        (1, 1, 2, 3)
        (1, 2, 1, 1)
        (1, 2, 1, 2)
        (1, 2, 1, 3)
        (1, 2, 2, 1)
        (1, 2, 2, 2)
        (1, 2, 2, 3)
        (1, 2, 3, 1)
        (1, 2, 3, 2)
        (1, 2, 3, 3)
        (1, 2, 3, 4)

    Return generator of tuples.
    '''

    if not mathtools.is_positive_integer(length):
        raise TypeError

    last_rgf = range(1, length + 1)

    rgf = length * [1]
    yield tuple(rgf)

    while not rgf == last_rgf:
        for i, x in enumerate(reversed(rgf)):
            if x < max(rgf[:-(i+1)]) + 1:
                first_part = rgf[:-(i+1)]
                increased_part = [rgf[-(i+1)] + 1]
                trailing_ones = i * [1]
                rgf = first_part + increased_part + trailing_ones
                yield tuple(rgf)
                break
