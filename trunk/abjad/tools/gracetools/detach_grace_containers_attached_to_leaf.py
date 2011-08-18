from abjad.tools.gracetools.get_grace_containers_attached_to_leaf import get_grace_containers_attached_to_leaf


def detach_grace_containers_attached_to_leaf(leaf):
    r'''.. versionadded:: 2.0

    Detach grace containers attached to `leaf`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> grace_container = gracetools.Grace([Note("cs'16")], kind = 'grace')
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

        abjad> gracetools.get_grace_containers_attached_to_leaf(staff[1])
        (Grace(cs'16),)

    ::

        abjad> gracetools.detach_grace_containers_attached_to_leaf(staff[1])
        (Grace(),)

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> gracetools.get_grace_containers_attached_to_leaf(staff[1])
        ()

    Return tuple.
    '''

    grace_containers = get_grace_containers_attached_to_leaf(leaf)

    for grace_container in grace_containers:
        grace_container.detach()

    return grace_containers
