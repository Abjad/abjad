from abjad.tools.contexttools.ContextMark import ContextMark


class StaffChangeMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of a staff change::

        abjad> piano_staff = scoretools.PianoStaff([])
        abjad> rh_staff = Staff("c'8 d'8 e'8 f'8")
        abjad> rh_staff.name = 'RHStaff'
        abjad> lh_staff = Staff("s2")
        abjad> lh_staff.name = 'LHStaff'
        abjad> piano_staff.extend([rh_staff, lh_staff])

    ::

        abjad> f(piano_staff)
        \new PianoStaff <<
            \context Staff = "RHStaff" {
                c'8
                d'8
                e'8
                f'8
            }
            \context Staff = "LHStaff" {
                s2
            }
        >>

    ::

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

    Staff change marks target staff context by default.
    '''

    _format_slot = 'opening'

    def __init__(self, staff, target_context = None):
        from abjad.tools.stafftools.Staff import Staff
        ContextMark.__init__(self, target_context = target_context)
        if self.target_context is None:
            self._target_context = Staff
        if not isinstance(staff, Staff):
            raise TypeError('staff change mark input value "%s" must be staff instance.' % str(staff))
        self._staff = staff

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self.staff, target_context = self.target_context)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self.staff is arg.staff
        return False

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return repr(self.staff)

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        r'''Read-only LilyPond format of staff change mark:

        ::

            abjad> staff = Staff("c'8 d'8 e'8 f'8")
            abjad> staff.name = 'RHStaff'
            abjad> staff_change = contexttools.StaffChangeMark(staff)
            abjad> staff_change.format
            '\\change Staff = RHStaff'

        Return string.
        '''
        return r'\change Staff = %s' % self.staff.name

    @apply
    def staff():
        def fget(self):
            r'''Get staff of staff change mark::

                abjad> rh_staff = Staff("c'8 d'8 e'8 f'8")
                abjad> rh_staff.name = 'RHStaff'
                abjad> staff_change = contexttools.StaffChangeMark(rh_staff)
                abjad> staff_change.staff
                Staff-"RHStaff"{4}

            Set staff of staff change mark::

                abjad> lh_staff = Staff("s2")
                abjad> lh_staff.name = 'LHStaff'
                abjad> staff_change.staff = lh_staff
                abjad> staff_change.staff
                Staff-"LHStaff"{1}

            Return staff.
            '''
            return self._staff
        def fset(self, staff):
            from abjad.tools.stafftools.Staff import Staff
            assert isinstance(staff, Staff)
            self._staff = staff
        return property(**locals())
