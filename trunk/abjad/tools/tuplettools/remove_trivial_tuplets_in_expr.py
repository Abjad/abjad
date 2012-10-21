from abjad.tools import componenttools


def remove_trivial_tuplets_in_expr(expr):
    r'''Remove trivial tuplets in `expr`::

        >>> tuplet_1 = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")
        >>> tuplet_2 = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8")
        >>> staff = Staff([tuplet_1, tuplet_2])

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            {
                c'8
                d'8
            }
        }

    ::

        >>> tuplettools.remove_trivial_tuplets_in_expr(staff)

    ::

        >>> f(staff)
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
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    for tuplet in list(iterationtools.iterate_components_in_expr(expr, tuplettools.Tuplet)):
        if tuplet.is_trivial:
            componenttools.move_parentage_and_spanners_from_components_to_components(
                [tuplet], tuplet[:])
