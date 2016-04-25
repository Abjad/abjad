# -*- coding: utf-8 -*-


def cumulative_signed_weights(sequence):
    r'''Cumulative signed weights of `sequence`.

    ::

        >>> l = [1, -2, -3, 4, -5, -6, 7, -8, -9, 10]
        >>> mathtools.cumulative_signed_weights(l)
        [1, -3, -6, 10, -15, -21, 28, -36, -45, 55]

    Raises type error when `sequence` is not a list.

    Use ``mathtools.cumulative_sums([abs(x) for x in l])``
    for cumulative (unsigned) weights

    Returns list.
    '''
    from abjad.tools import mathtools

    if not isinstance(sequence, list):
        raise TypeError

    result = []

    for x in sequence:
        try:
            next_element = abs(previous) + abs(x)
            previous_sign = mathtools.sign(previous)
        except NameError:
            next_element = abs(x)
            previous_sign = 0
        sign_x = mathtools.sign(x)
        if sign_x == -1:
            next_element *= sign_x
        elif sign_x == 0:
            next_element *= previous_sign
        result.append(next_element)
        previous = next_element

    return result
