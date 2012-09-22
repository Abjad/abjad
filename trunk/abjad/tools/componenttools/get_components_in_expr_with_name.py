def get_components_in_expr_with_name(expr, name):
    r'''.. versionadded:: 2.9

    Get components in `expr` with `name`::

        >>> staff = Staff(r"\new Voice { c'8 d'8 } \new Voice { e'8 f'8 } \new Voice { g'4 }")
        >>> staff[0].name = 'outer voice'
        >>> staff[1].name = 'middle voice'
        >>> staff[2].name = 'outer voice'

        >>> f(staff)
        \new Staff {
            \context Voice = "outer voice" {
                c'8
                d'8
            }
            \context Voice = "middle voice" {
                e'8
                f'8
            }
            \context Voice = "outer voice" {
                g'4
            }
        }

        >>> componenttools.get_components_in_expr_with_name(staff, 'outer voice')
        [Voice-"outer voice"{2}, Voice-"outer voice"{1}]

    ::

        >>> componenttools.get_components_in_expr_with_name(staff, 'middle voice')
        [Voice-"middle voice"{2}]

    Return list of zero or more components found.
    '''
    from abjad.tools import iterationtools

    result = []
    
    for component in iterationtools.iterate_components_in_expr(expr):
        if name is None or getattr(component, 'name', None) == name:
            result.append(component)

    return result
