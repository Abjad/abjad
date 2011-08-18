from __future__ import division
from fractions import Fraction
from numbers import Number


def divide_number_by_ratio(number, ratio):
    '''Divide integer by `ratio`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.divide_number_by_ratio(1, [1, 1, 3])
        [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

    Divide fraction by `ratio`::

        abjad> mathtools.divide_number_by_ratio(Fraction(1), [1, 1, 3])
        [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

    Divide float by ratio::

        abjad> mathtools.divide_number_by_ratio(1.0, [1, 1, 3]) # doctest: +SKIP
        [0.20000000000000001, 0.20000000000000001, 0.60000000000000009]

    Raise type error on nonnumeric `number`.

    Raise type error on noninteger in `ratio`.

    Return list of fractions or list of floats.

    .. versionchanged:: 2.0
        renamed ``mathtools.divide_number_by_ratio()`` to
        ``mathtools.divide_number_by_ratio()``.
    '''

    if not isinstance(number, Number):
        raise TypeError('number "%s" be number.' % str(number))

    if not all([isinstance(part, int) for part in ratio]):
        raise TypeError('ratio "%s" must comprise only integers.' % str(ratio))

    try:
        factor = Fraction(number, sum(ratio))
    except TypeError:
        factor = number / sum(ratio)

    return [p * factor for p in ratio]
