from abjad.tools import componenttools


def remove_trivial_tuplets_in_expr(expr):
    r'''Remove trivial tuplets in `expr`::

        >>> t = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")
        >>> u = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8")
        >>> s = Staff([t, u])
        >>> len(s)
        2

    ::

        >>> s[0]
        FixedDurationTuplet(1/4, [c'8, d'8, e'8])
        >>> s[1]
        FixedDurationTuplet(1/4, [c'8, d'8])

    ::

        >>> tuplettools.remove_trivial_tuplets_in_expr(s)
        >>> len(s)
        3
        >>> s[0]
        FixedDurationTuplet(1/4, [c'8, d'8, e'8])
        >>> s[1]
        Note("c'8")
        >>> s[2]
        Note("d'8")

    ::

        >>> f(s)
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
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    for tuplet in list(iterationtools.iterate_components_in_expr(expr, tuplettools.Tuplet)):
        if tuplet.is_trivial:
            componenttools.move_parentage_and_spanners_from_components_to_components(
                [tuplet], tuplet[:])
