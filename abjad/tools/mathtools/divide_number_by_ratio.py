# -*- coding: utf-8 -*-
import numbers
from abjad import Fraction


def divide_number_by_ratio(number, ratio):
    r'''Divides `number` by `ratio`.

    ..  container:: example

        ::

            >>> mathtools.divide_number_by_ratio(1, [1, 1, 3])
            [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

        ::

            >>> mathtools.divide_number_by_ratio(Fraction(1), [1, 1, 3])
            [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

        ::

            >>> mathtools.divide_number_by_ratio(1.0, [1, 1, 3]) # doctest: +SKIP
            [0.20000000000000001, 0.20000000000000001, 0.60000000000000009]

    Returns list of fractions or list of floats.
    '''
    from abjad.tools import mathtools
    assert isinstance(number, numbers.Number)
    ratio = mathtools.Ratio(ratio)
    denominator = sum(ratio.numbers)
    factors = [Fraction(_, denominator) for _ in ratio.numbers]
    result = [_ * number for _ in factors]
    return result
