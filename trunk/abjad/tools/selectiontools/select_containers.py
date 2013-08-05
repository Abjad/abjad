# -*- encoding: utf-8 -*-
def select_containers(expr=None):
    r'''Select containers in `expr`.

    Example 1. Select containers in staff, including staff:

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

        >>> selection = selectiontools.select_containers(staff)

    ::
        
        >>> selection
        FreeContainerSelection(...)

    ::

        >>> for container in selection:
        ...     container
        Staff{6}
        Tuplet(2/3, [e'8, g'8, f'8])
        Tuplet(2/3, [e'8, c'8, d'8])

    Return free container selection.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import selectiontools
    expr = expr or []
    containers = iterationtools.iterate_containers_in_expr(expr)
    selection = selectiontools.FreeContainerSelection(music=containers)
    return selection
