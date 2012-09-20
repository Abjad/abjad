def detach_grace_containers_attached_to_leaves_in_expr(expr, kind=None):
    r'''.. versionadded:: 2.9

    Detach grace containers attached to leaves in `expr`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> grace_container = gracetools.GraceContainer([Note("cs'16")], kind='grace')
        >>> grace_container(staff[1])
        Note("d'8")

    ::

        >>> f(staff)
        \new Staff {
            c'8
            \grace {
                cs'16
            }
            d'8
            e'8
            f'8
        }

    ::

        >>> gracetools.detach_grace_containers_attached_to_leaves_in_expr(staff)
        (GraceContainer(),)

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Return tuple of zero or more grace containers.
    '''
    from abjad.tools import gracetools
    from abjad.tools import iterationtools

    result = []
    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        result.extend(gracetools.detach_grace_containers_attached_to_leaf(leaf, kind=kind))

    return tuple(result)
