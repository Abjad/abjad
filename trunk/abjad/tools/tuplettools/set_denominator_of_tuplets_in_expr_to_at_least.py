from abjad.tools import durationtools
from abjad.tools import mathtools


def set_denominator_of_tuplets_in_expr_to_at_least(expr, n):
    r'''.. versionadded:: 2.0

    Set denominator of tuplets in `expr` to at least `n`::

        >>> tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")

    ::

        >>> f(tuplet)
        \fraction \times 3/5 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }

    ::

        >>> tuplettools.set_denominator_of_tuplets_in_expr_to_at_least(tuplet, 8)

    ::

        >>> f(tuplet)
        \fraction \times 6/10 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }

    Return none.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    assert mathtools.is_nonnegative_integer_power_of_two(n)
    for tuplet in iterationtools.iterate_tuplets_in_expr(expr):
        tuplet.force_fraction = True
        durations = [tuplet.contents_duration, tuplet.preprolated_duration, (1, n)]
        duration_pairs = durationtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
            durations)
        tuplet.preferred_denominator = duration_pairs[1][0]
