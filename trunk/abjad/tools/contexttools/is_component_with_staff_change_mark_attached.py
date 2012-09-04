def is_component_with_staff_change_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with staff change mark attached::

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

        >>> contexttools.is_component_with_staff_change_mark_attached(rh_staff[2])
        True

    Otherwise false::

        >>> contexttools.is_component_with_staff_change_mark_attached(rh_staff)
        False

    Return boolean.
    '''
    from abjad.tools import contexttools

    return contexttools.is_component_with_context_mark_attached(expr, klasses=(contexttools.StaffChangeMark,))
