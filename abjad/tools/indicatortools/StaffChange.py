# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class StaffChange(AbjadObject):
    r'''A staff change.

    ::

        >>> staff_group = StaffGroup()
        >>> staff_group.context_name = 'PianoStaff'
        >>> rh_staff = Staff("c'8 d'8 e'8 f'8")
        >>> rh_staff.name = 'RHStaff'
        >>> lh_staff = Staff("s2")
        >>> lh_staff.name = 'LHStaff'
        >>> staff_group.extend([rh_staff, lh_staff])
        >>> staff_change = indicatortools.StaffChange(lh_staff)
        >>> attach(staff_change, rh_staff[2])
        >>> show(staff_group) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff_group)
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

    '''

    ### CLASS VARIABLES ###

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, staff=None):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Staff
        if not isinstance(staff, (scoretools.Staff, type(None))):
            message = 'staff change input value {!r}'
            message += ' must be staff instance.'
            message.format(staff)
            raise TypeError(message)
        self._staff = staff

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies staff change.

        Returns new staff change.
        '''
        return type(self)(self.staff)

    def __eq__(self, arg):
        r'''Is true when `arg` is a staff change with a staff value equal 
        to that of this staff change. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self.staff is arg.staff
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.staff)

    @property
    def _lilypond_format(self):
        return r'\change Staff = {}'.format(self.staff.name)

    ### PUBLIC PROPERTIES ###

    @property
    def staff(self):
        r'''Staff of staff change.

        ::

            >>> staff_change.staff
            Staff('s2')

        Returns staff.
        '''
        return self._staff
