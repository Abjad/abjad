from abjad.tools import componenttools


def get_first_container_in_proper_parentage_of_component(component):
    r'''.. versionadded:: 2.0

    Get first container in proper parentage of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> containertools.get_first_container_in_proper_parentage_of_component(staff[1])
        Staff{4}

    Return container or none.
    '''
    from abjad.tools import containertools

    return componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
        component, containertools.Container)
