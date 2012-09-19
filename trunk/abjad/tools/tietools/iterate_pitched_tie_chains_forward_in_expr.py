def iterate_pitched_tie_chains_forward_in_expr(expr):
    r'''.. versionadded:: 2.9

    .. note: Deprecated. Use `tietools.iterate_pitched_tie_chains_in_expr` instead.

    Iterate pitched tie chains forward in `expr`::

        >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 r8 f'8 ~ f'16 r8.")

    ::

        >>> f(staff)
        \new Staff {
            c'4 ~
            \times 2/3 {
                c'16
                d'8
            }
            e'8
            r8
            f'8 ~
            f'16
            r8.
        }

    ::

        >>> for x in tietools.iterate_pitched_tie_chains_forward_in_expr(staff): x
        ... 
        TieChain((Note("c'4"), Note("c'16")))
        TieChain((Note("d'8"),))
        TieChain((Note("e'8"),))
        TieChain((Note("f'8"), Note("f'16")))

    Tie chains are pitched if they comprise notes or chords.

    Tie chains are not pitched if they comprise rests or skips.

    Return generator.
    '''
    from abjad.tools import tietools

    return tietools.iterate_pitched_tie_chains_in_expr(expr)
