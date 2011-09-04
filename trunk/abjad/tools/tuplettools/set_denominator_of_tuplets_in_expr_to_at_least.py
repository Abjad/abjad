from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.tuplettools.iterate_tuplets_forward_in_expr import iterate_tuplets_forward_in_expr


def set_denominator_of_tuplets_in_expr_to_at_least(expr, n):
    r'''.. versionadded:: 2.0

    Set denominator of tuplets in `expr` to at least `n`::

        abjad> tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")

    ::

        abjad> f(tuplet)
        \fraction \times 3/5 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }

    ::

        abjad> tuplettools.set_denominator_of_tuplets_in_expr_to_at_least(tuplet, 8)

    ::

        abjad> f(tuplet)
        \fraction \times 6/10 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }

    Return none.
    '''

    assert mathtools.is_nonnegative_integer_power_of_two(n)
    for tuplet in iterate_tuplets_forward_in_expr(expr):
        tuplet.force_fraction = True
        durations = [tuplet.contents_duration, tuplet.preprolated_duration, (1, n)]
        duration_pairs = durationtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
            durations)
        tuplet.preferred_denominator = duration_pairs[1][0]
