from abjad.tools.stafftools.Staff import Staff
from abjad.tools import componenttools


def get_first_staff_in_proper_parentage_of_component(component):
    r'''.. versionadded:: 2.0

    Get first staff in proper parentage of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> stafftools.get_first_staff_in_proper_parentage_of_component(staff[1])
        Staff{4}

    Return staff or none.
    '''

    return componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
        component, Staff)
