from abjad.tools.durationtools.yield_all_positive_integer_pairs_in_cantor_diagonalized_order import yield_all_positive_integer_pairs_in_cantor_diagonalized_order
from fractions import Fraction


def yield_all_positive_rationals_in_cantor_diagonalized_order_uniquely():
    r'''.. versionadded:: 2.0

    Yield all positive rationals in Cantor diagonalized order uniquely::

        abjad> from abjad.tools import durationtools

    ::

        abjad> generator = durationtools.yield_all_positive_rationals_in_cantor_diagonalized_order_uniquely()
        abjad> for n in range(16):
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

    generator = yield_all_positive_integer_pairs_in_cantor_diagonalized_order()
    while True:
        integer_pair = generator.next()
        rational = Fraction(*integer_pair)
        if (rational.numerator, rational.denominator) == integer_pair:
            yield rational
