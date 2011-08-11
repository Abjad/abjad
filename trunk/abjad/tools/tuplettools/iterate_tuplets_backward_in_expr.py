from abjad.tools.tuplettools.Tuplet import Tuplet
from abjad.tools.componenttools.iterate_components_backward_in_expr import iterate_components_backward_in_expr


def iterate_tuplets_backward_in_expr(expr, start = 0, stop = None):
    r'''.. versionadded:: 2.0

    Iterate tuplets backward in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        abjad> Tuplet(Fraction(2, 3), staff[:3])
        Tuplet(2/3, [c'8, d'8, e'8])
        abjad> Tuplet(Fraction(2, 3), staff[-3:])
        Tuplet(2/3, [a'8, b'8, c''8])

        abjad> f(staff)
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            f'8
            g'8
            \times 2/3 {
                a'8
                b'8
                c''8
            }
        }

        abjad> for tuplet in tuplettools.iterate_tuplets_backward_in_expr(staff):
        ...     tuplet
        ...
        Tuplet(2/3, [a'8, b'8, c''8])
        Tuplet(2/3, [c'8, d'8, e'8])

    Return generator.
    '''

    return iterate_components_backward_in_expr(expr, Tuplet, start = start, stop = stop)
