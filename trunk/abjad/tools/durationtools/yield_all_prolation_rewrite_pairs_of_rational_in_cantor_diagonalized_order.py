from abjad.tools.durationtools.yield_all_assignable_rationals_in_cantor_diagonalized_order import yield_all_assignable_rationals_in_cantor_diagonalized_order
from fractions import Fraction


def yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(
    prolated_duration, minimum_written_duration = Fraction(1, 128)):
    r'''.. versionadded:: 2.0

    Yield all prolation rewrite pairs of `prolated_duration` in Cantor diagonalized order.

    Ensure written duration never less than `minimum_written_duration`.

    The different ways to notate a prolated duration of ``1/8``::

        abjad> from abjad.tools import durationtools

    ::

        abjad> pairs = durationtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Fraction(1, 8))
        abjad> for pair in pairs: pair
        ...
        (Fraction(1, 1), Fraction(1, 8))
        (Fraction(2, 3), Fraction(3, 16))
        (Fraction(4, 3), Fraction(3, 32))
        (Fraction(4, 7), Fraction(7, 32))
        (Fraction(8, 7), Fraction(7, 64))
        (Fraction(8, 15), Fraction(15, 64))
        (Fraction(16, 15), Fraction(15, 128))
        (Fraction(16, 31), Fraction(31, 128))

    The different ways to notate a prolated duration of ``1/12``. ::

        abjad> pairs = durationtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Fraction(1, 12))
        abjad> for pair in pairs: pair
        ...
        (Fraction(2, 3), Fraction(1, 8))
        (Fraction(4, 3), Fraction(1, 16))
        (Fraction(8, 9), Fraction(3, 32))
        (Fraction(16, 9), Fraction(3, 64))
        (Fraction(16, 21), Fraction(7, 64))
        (Fraction(32, 21), Fraction(7, 128))
        (Fraction(32, 45), Fraction(15, 128))

    The different ways to notate a prolated duration of ``5/48``. ::

        abjad> pairs = durationtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Fraction(5, 48))
        abjad> for pair in pairs: pair
        ...
        (Fraction(5, 6), Fraction(1, 8))
        (Fraction(5, 3), Fraction(1, 16))
        (Fraction(5, 9), Fraction(3, 16))
        (Fraction(10, 9), Fraction(3, 32))
        (Fraction(20, 21), Fraction(7, 64))
        (Fraction(40, 21), Fraction(7, 128))
        (Fraction(8, 9), Fraction(15, 128))

    Return generator of paired fractions.
    '''
    from abjad.tools.tuplettools.is_proper_tuplet_multiplier import is_proper_tuplet_multiplier

    generator = yield_all_assignable_rationals_in_cantor_diagonalized_order()
    pairs = []

    while True:
        written_duration = generator.next()
        if written_duration < minimum_written_duration:
            pairs = tuple(pairs)
            return pairs
        prolation = prolated_duration / written_duration
        if is_proper_tuplet_multiplier(prolation):
            pair = (prolation, written_duration)
            pairs.append(pair)
