from abjad.tools.contexttools.StaffChangeMark import StaffChangeMark
from abjad.tools.contexttools.get_effective_context_mark import get_effective_context_mark


def get_effective_staff(component):
    '''.. versionadded:: 2.0

    Get effective staff of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> staff.name = 'First Staff'

    ::

        abjad> f(staff)
        \context Staff = "First Staff" {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> for note in staff:
        ...     print note, contexttools.get_effective_staff(note)
        ...
        c'8 Staff-"First Staff"{4}
        d'8 Staff-"First Staff"{4}
        e'8 Staff-"First Staff"{4}
        f'8 Staff-"First Staff"{4}

    Return staff or none.
    '''
    from abjad.tools.stafftools.Staff import Staff
    from abjad.tools import componenttools

    staff_change_mark = get_effective_context_mark(component, StaffChangeMark)
    if staff_change_mark is not None:
        return staff_change_mark.staff

    return componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(component, Staff)
