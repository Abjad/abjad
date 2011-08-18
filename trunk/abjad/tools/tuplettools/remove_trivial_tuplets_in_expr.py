from abjad.tools.tuplettools.Tuplet import Tuplet
from abjad.tools import componenttools


def remove_trivial_tuplets_in_expr(expr):
    r'''Remove trivial tuplets in `expr`::

        abjad> t = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")
        abjad> u = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8")
        abjad> s = Staff([t, u])
        abjad> len(s)
        2

    ::

        abjad> s[0]
        FixedDurationTuplet(1/4, [c'8, d'8, e'8])
        abjad> s[1]
        FixedDurationTuplet(1/4, [c'8, d'8])

    ::

        abjad> tuplettools.remove_trivial_tuplets_in_expr(s)
        abjad> len(s)
        3
        abjad> s[0]
        FixedDurationTuplet(1/4, [c'8, d'8, e'8])
        abjad> s[1]
        Note("c'8")
        abjad> s[2]
        Note("d'8")

    ::

        abjad> f(s)
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            c'8
            d'8
        }

    Replace trivial tuplets with plain leaves.

    Return none.

    .. versionchanged:: 2.0
        renamed ``tuplettools.slip_trivial()`` to
        ``tuplettools.remove_trivial_tuplets_in_expr()``.
    '''

    for tuplet in list(componenttools.iterate_components_forward_in_expr(expr, Tuplet)):
        if tuplet.is_trivial:
            componenttools.move_parentage_and_spanners_from_components_to_components(
                [tuplet], tuplet[:])
