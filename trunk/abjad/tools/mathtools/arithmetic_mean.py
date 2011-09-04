from fractions import Fraction


def arithmetic_mean(sequence):
    '''.. versionadded:: 1.1

    Arithmetic means of `sequence` as an exact integer::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.arithmetic_mean([1, 2, 2, 20, 30])
        11

    As a rational::

        abjad> mathtools.arithmetic_mean([1, 2, 20])
        Fraction(23, 3)

    As a float::

        abjad> mathtools.arithmetic_mean([2, 2, 20.0])
        8.0

    Return number.

    .. versionchanged:: 2.0
        renamed ``sequencetools.arithmetic_mean()`` to
        ``mathtools.arithmetic_mean()``.
    '''

    sum_l = sum(sequence)
    len_l = len(sequence)

    if isinstance(sum_l, float):
        return sum_l / len_l

    result = Fraction(sum(sequence), len(sequence))

    int_result = int(result)
    if int_result == result:
        return int_result
    else:
        return result
