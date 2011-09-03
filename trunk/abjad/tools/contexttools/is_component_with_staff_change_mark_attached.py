from abjad.tools.contexttools.StaffChangeMark import StaffChangeMark
from abjad.tools.contexttools.is_component_with_context_mark_attached import is_component_with_context_mark_attached


def is_component_with_staff_change_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with staff change mark attached::

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

        abjad> contexttools.is_component_with_staff_change_mark_attached(rh_staff[2])
        True

    Otherwise false::

        abjad> contexttools.is_component_with_staff_change_mark_attached(rh_staff)
        False

    Return boolean.
    '''

    return is_component_with_context_mark_attached(expr, klasses=(StaffChangeMark,))
