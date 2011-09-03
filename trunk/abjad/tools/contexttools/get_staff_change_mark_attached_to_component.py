from abjad.tools.contexttools.StaffChangeMark import StaffChangeMark
from abjad.tools.contexttools.get_context_mark_attached_to_component import get_context_mark_attached_to_component


def get_staff_change_mark_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get staff change mark attached to `component`::

        abjad> piano_staff = scoretools.PianoStaff([])
        abjad> rh_staff = Staff("c'8 d'8 e'8 f'8")
        abjad> rh_staff.name = 'RHStaff'
        abjad> lh_staff = Staff("s2")
        abjad> lh_staff.name = 'LHStaff'
        abjad> piano_staff.extend([rh_staff, lh_staff])
        abjad> contexttools.StaffChangeMark(lh_staff)(rh_staff[2])
        StaffChangeMark(Staff-"LHStaff"{1})(e'8)

    ::

        abjad> f(piano_staff)
        \new PianoStaff <<
            \context Staff = "RHStaff" {
                c'8
                d'8
                \change Staff = LHStaff
                e'8
                f'8
            }
            \context Staff = "LHStaff" {
                s2
            }
        >>

    ::

        abjad> contexttools.get_staff_change_mark_attached_to_component(rh_staff[2])
        StaffChangeMark(Staff-"LHStaff"{1})(e'8)

    Return staff change mark.

    Raise missing mark error when no staff change mark attaches to `component`.
    '''

    return get_context_mark_attached_to_component(component, klasses=(StaffChangeMark,))
