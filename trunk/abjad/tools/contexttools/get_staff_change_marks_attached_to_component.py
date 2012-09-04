def get_staff_change_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get staff change marks attached to `component`::

        >>> piano_staff = scoretools.PianoStaff([])
        >>> rh_staff = Staff("c'8 d'8 e'8 f'8")
        >>> rh_staff.name = 'RHStaff'
        >>> lh_staff = Staff("s2")
        >>> lh_staff.name = 'LHStaff'
        >>> piano_staff.extend([rh_staff, lh_staff])
        >>> contexttools.StaffChangeMark(lh_staff)(rh_staff[2])
        StaffChangeMark(Staff-"LHStaff"{1})(e'8)

    ::

        >>> f(piano_staff)
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

        >>> contexttools.get_staff_change_marks_attached_to_component(rh_staff[2])
        (StaffChangeMark(Staff-"LHStaff"{1})(e'8),)

    Return tuple of zero or more staff change marks.
    '''
    from abjad.tools import contexttools

    return contexttools.get_context_marks_attached_to_component(component, klasses=(contexttools.StaffChangeMark,))
