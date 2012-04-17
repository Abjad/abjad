from abjad.tools.gracetools.detach_grace_containers_attached_to_leaf import detach_grace_containers_attached_to_leaf


def detach_grace_containers_attached_to_leaves_in_expr(expr):
    r'''.. versionadded:: 2.9

    Detach grace containers attached to leaves in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> grace_container = gracetools.GraceContainer([Note("cs'16")], kind='grace')
        abjad> grace_container(staff[1])
        Note("d'8")

    ::

        abjad> f(staff)
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

        abjad> gracetools.detach_grace_containers_attached_to_leaves_in_expr(staff)
        (GraceContainer(),)

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Return tuple of zero or more grace containers.
    '''
    from abjad.tools import leaftools

    result = []
    for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
        result.extend(detach_grace_containers_attached_to_leaf(leaf))

    return tuple(result)
