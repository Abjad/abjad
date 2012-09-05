from abjad.tools import componenttools


def iterate_tuplets_forward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    Iterate tuplets forward in `expr`::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> Tuplet(Fraction(2, 3), staff[:3])
        Tuplet(2/3, [c'8, d'8, e'8])
        >>> Tuplet(Fraction(2, 3), staff[-3:])
        Tuplet(2/3, [a'8, b'8, c''8])

        >>> f(staff)
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

        >>> for tuplet in tuplettools.iterate_tuplets_forward_in_expr(staff):
        ...     tuplet
        ...
        Tuplet(2/3, [c'8, d'8, e'8])
        Tuplet(2/3, [a'8, b'8, c''8])

    Return generator.
    '''
    from abjad.tools import tuplettools

    return componenttools.iterate_components_forward_in_expr(expr, tuplettools.Tuplet, start=start, stop=stop)
