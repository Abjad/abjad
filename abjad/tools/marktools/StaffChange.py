# -*- encoding: utf-8 -*-
from abjad.tools.marktools.ContextMark import ContextMark


class StaffChange(ContextMark):
    r'''A staff change.

    ::

        >>> piano_staff = scoretools.PianoStaff([])
        >>> rh_staff = Staff("c'8 d'8 e'8 f'8")
        >>> rh_staff.name = 'RHStaff'
        >>> lh_staff = Staff("s2")
        >>> lh_staff.name = 'LHStaff'
        >>> piano_staff.extend([rh_staff, lh_staff])

    ..  doctest::

        >>> f(piano_staff)
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

        >>> show(piano_staff) # doctest: +SKIP

    ::

        >>> staff_change = marktools.StaffChange(lh_staff)
        >>> attach(staff_change, rh_staff[2])
        >>> show(piano_staff) # doctest: +SKIP

    ..  doctest::

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

    Staff change marks target staff context by default.
    '''

    ### CLASS VARIABLES ###

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, staff=None, _target_context=None):
        from abjad.tools import scoretools
        _target_context = _target_context or scoretools.Staff
        ContextMark.__init__(self, _target_context=_target_context)
        if not isinstance(staff, (scoretools.Staff, type(None))):
            message = 'staff change mark input value {!r}'
            message += ' must be staff instance.'
            message.format(staff)
            raise TypeError(message)
        self._staff = staff

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(self.staff, _target_context=self._target_context)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self.staff is arg.staff
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.staff)

    @property
    def _lilypond_format(self):
        return r'\change Staff = %s' % self.staff.name

    ### PUBLIC PROPERTIES ###

    @apply
    def staff():
        def fget(self):
            r'''Get staff of staff change mark:

            ::

                >>> rh_staff = Staff("c'8 d'8 e'8 f'8")
                >>> rh_staff.name = 'RHStaff'
                >>> staff_change = marktools.StaffChange(rh_staff)
                >>> staff_change.staff
                Staff-"RHStaff"{4}

            Set staff of staff change mark:

            ::

                >>> lh_staff = Staff("s2")
                >>> lh_staff.name = 'LHStaff'
                >>> staff_change.staff = lh_staff
                >>> staff_change.staff
                Staff-"LHStaff"{1}

            Returns staff.
            '''
            return self._staff
        def fset(self, staff):
            from abjad.tools.scoretools.Staff import Staff
            assert isinstance(staff, Staff)
            self._staff = staff
        return property(**locals())
