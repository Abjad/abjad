from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.constants import *


class StaffChange(AbjadValueObject):
    r'''Staff change.

    ..  container:: example

        Explicit staff change:

        >>> staff_group = abjad.StaffGroup()
        >>> staff_group.context_name = 'PianoStaff'
        >>> rh_staff = abjad.Staff("c'8 d'8 e'8 f'8", name='RHStaff')
        >>> lh_staff = abjad.Staff("s2", name='LHStaff')
        >>> staff_group.extend([rh_staff, lh_staff])
        >>> staff_change = abjad.StaffChange(lh_staff)
        >>> abjad.attach(staff_change, rh_staff[2])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff_group)
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
        '_context',
        '_staff',
        )

    _format_leaf_children = False

    _format_slot = 'opening'

    _time_orientation = Right

    ### INITIALIZER ###

    def __init__(self, staff=None):
        import abjad
        self._context = 'Staff'
        if not isinstance(staff, (abjad.Staff, type(None))):
            message = 'staff change input value {!r}'
            message += ' must be staff instance.'
            message.format(staff)
            raise TypeError(message)
        self._staff = staff

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of staff change.

        ..  container:: example

            Default staff change:

            >>> staff_change = abjad.StaffChange()
            >>> print(str(staff_change))
            \change Staff = ##f

        ..  container:: example

            Explicit staff change:

            >>> lh_staff = abjad.Staff("s2", name='LHStaff')
            >>> staff_change = abjad.StaffChange(staff=lh_staff)
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

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.staff)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of staff change.

        ..  container:: example

            Default staff change:

            >>> staff_change = abjad.StaffChange()
            >>> staff_change.context
            'Staff'

        ..  container:: example

            Explicit staff change:

            >>> lh_staff = abjad.Staff("s2", name='LHStaff')
            >>> staff_change = abjad.StaffChange(staff=lh_staff)
            >>> staff_change.context
            'Staff'

        Returns context or string.
        '''
        return self._context

    @property
    def staff(self):
        r'''Gets staff of staff change.

        ..  container:: example

            Default staff change:

            >>> staff_change = abjad.StaffChange()
            >>> staff_change.staff is None
            True

        ..  container:: example

            Explicit staff change:

            >>> lh_staff = abjad.Staff("s2", name='LHStaff')
            >>> staff_change = abjad.StaffChange(staff=lh_staff)
            >>> staff_change.staff
            Staff('s2', name='LHStaff')

        Set to staff or none.

        Defaults to none.

        Returns staff or none.
        '''
        return self._staff
