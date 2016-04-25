# -*- coding: utf-8 -*-
import fractions


def arithmetic_mean(sequence):
    '''Arithmetic means of `sequence` as an exact integer.

    ::

        >>> mathtools.arithmetic_mean([1, 2, 2, 20, 30])
        11

    As a rational:

    ::

        >>> mathtools.arithmetic_mean([1, 2, 20])
        Fraction(23, 3)

    As a float:

    ::

        >>> mathtools.arithmetic_mean([2, 2, 20.0])
        8.0

    Returns number.
    '''

    sum_l = sum(sequence)
    len_l = len(sequence)

    if isinstance(sum_l, float):
        return sum_l / len_l

    result = fractions.Fraction(sum(sequence), len(sequence))

    int_result = int(result)
    if int_result == result:
        return int_result
    else:
        return result
