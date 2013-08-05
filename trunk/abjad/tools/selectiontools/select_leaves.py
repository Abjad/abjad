# -*- encoding: utf-8 -*-
def select_leaves(expr=None):
    r'''Select leaves in `expr`.

    ..  container:: example
    
        **Example.** Select leaves in staff:

        ::

            >>> staff = Staff()
            >>> staff.extend(r"c'8 d'8 \times 2/3 { e'8 g'8 f'8 }")
            >>> staff.extend(r"g'8 f'8 \times 2/3 { e'8 c'8 d'8 }")
            >>> show(staff) # doctest: +SKIP

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

            >>> selection = selectiontools.select_leaves(staff)

        ::
            
            >>> selection
            FreeLeafSelection(...)

        ::

            >>> for leaf in selection:
            ...     leaf
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("g'8")
            Note("f'8")
            Note("g'8")
            Note("f'8")
            Note("e'8")
            Note("c'8")
            Note("d'8")

    Return free leaf selection.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import selectiontools
    expr = iterationtools.iterate_leaves_in_expr(expr)
    selection = selectiontools.FreeLeafSelection(music=expr)
    return selection

