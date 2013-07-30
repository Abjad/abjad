def select_tuplets(expr=None):
    r'''Select tuplets in `expr`.

        >>> staff = Staff()
        >>> staff.extend(r"c'8 d'8 \times 2/3 { e'8 g'8 f'8 }")
        >>> staff.extend(r"g'8 f'8 \times 2/3 { e'8 c'8 d'8 }")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            \times 2/3 {
                e'8
                g'8
                f'8
            }
            g'8
            f'8
            \times 2/3 {
                e'8
                c'8
                d'8
            }
        }


    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> selection = selectiontools.select_tuplets(staff)

    ::

        >>> selection
        TupletSelection(...)

    ::

        >>> for tuplet in selection:
        ...     tuplet
        Tuplet(2/3, [e'8, g'8, f'8])
        Tuplet(2/3, [e'8, c'8, d'8])

    Return tuplet selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools
    from abjad.tools import selectiontools
    expr = expr or []
    tuplets = iterationtools.iterate_tuplets_in_expr(expr)
    selection = selectiontools.TupletSelection(music=tuplets)
    return selection
