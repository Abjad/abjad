# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class StaffChange(AbjadValueObject):
    r'''A staff change.

    ..  container:: example

        **Example 1.** Explicit staff change:

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

            >>> print(format(staff_group))
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

    __slots__ = (
        '_default_scope',
        '_staff',
        )

    _format_leaf_children = False

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

    def __str__(self):
        r'''Gets string representation of staff change.

        ..  container:: example

            **Example 1.** Default staff change:

            ::

                >>> staff_change = indicatortools.StaffChange()
                >>> print(str(staff_change))
                \change Staff = ##f

        ..  container:: example

            **Example 2.** Explicit staff change:
    
            ::

                >>> staff_change = indicatortools.StaffChange(staff=lh_staff)
                >>> print(str(staff_change))
                \change Staff = LHStaff

        Returns string.
        '''
        from abjad.tools import schemetools
        if self.staff is None:
            return r'\change Staff = ##f'
        return r'\change Staff = {}'.format(
            schemetools.Scheme.format_scheme_value(self.staff.name),
            )

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.opening.commands.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.staff)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of staff change.

        ..  container:: example

            **Example 1.** Default staff change:

            ::

                >>> staff_change = indicatortools.StaffChange()
                >>> staff_change.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        ..  container:: example

            **Example 2.** Explicit staff change:
    
            ::

                >>> staff_change = indicatortools.StaffChange(staff=lh_staff)
                >>> staff_change.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        Staff changes are staff-scoped.

        Returns staff.
        '''
        return self._default_scope

    @property
    def staff(self):
        r'''Gets staff of staff change.

        ..  container:: example

            **Example 1.** Default staff change:

            ::

                >>> staff_change = indicatortools.StaffChange()
                >>> staff_change.staff is None
                True

        ..  container:: example

            **Example 2.** Explicit staff change:
    
            ::

                >>> staff_change = indicatortools.StaffChange(staff=lh_staff)
                >>> staff_change.staff
                Staff('s2')
        
        Set to staff or none.

        Defaults to none.

        Returns staff or none.
        '''
        return self._staff
