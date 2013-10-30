# -*- encoding: utf-8 -*-
from abjad.tools import scoretools


def iterate_tuplets_in_expr(expr, reverse=False, start=0, stop=None):
    r'''Iterates tuplets in `expr`.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> Tuplet(Multiplier(2, 3), staff[:3])
        Tuplet(2/3, [c'8, d'8, e'8])
        >>> Tuplet(Multiplier(2, 3), staff[-3:])
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

        >>> for tuplet in iterationtools.iterate_tuplets_in_expr(staff):
        ...     tuplet
        ...
        Tuplet(2/3, [c'8, d'8, e'8])
        Tuplet(2/3, [a'8, b'8, c''8])

    Iterate tuplets backward in `expr`:

    ::

        >>> for tuplet in iterationtools.iterate_tuplets_in_expr(
        ...     staff, reverse=True):
        ...     tuplet
        ...
        Tuplet(2/3, [a'8, b'8, c''8])
        Tuplet(2/3, [c'8, d'8, e'8])

    Iterates across different logical voices.

    Returns generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr,
        component_class=scoretools.Tuplet,
        reverse=reverse,
        start=start,
        stop=stop,
        )
