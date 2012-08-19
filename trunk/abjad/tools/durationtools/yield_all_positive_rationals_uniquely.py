import fractions


def yield_all_positive_rationals_uniquely():
    r'''.. versionadded:: 2.0

    Yield all positive rationals in Cantor diagonalized order uniquely::

        >>> generator = durationtools.yield_all_positive_rationals_uniquely()
        >>> for n in range(16):
        ...     generator.next()
        ...
        Fraction(1, 1)
        Fraction(2, 1)
        Fraction(1, 2)
        Fraction(1, 3)
        Fraction(3, 1)
        Fraction(4, 1)
        Fraction(3, 2)
        Fraction(2, 3)
        Fraction(1, 4)
        Fraction(1, 5)
        Fraction(5, 1)
        Fraction(6, 1)
        Fraction(5, 2)
        Fraction(4, 3)
        Fraction(3, 4)
        Fraction(2, 5)

    Return fraction generator.
    '''
    from abjad.tools import durationtools

    generator = durationtools.yield_all_positive_integer_pairs()
    while True:
        integer_pair = generator.next()
        rational = fractions.Fraction(*integer_pair)
        if (rational.numerator, rational.denominator) == integer_pair:
            yield rational
