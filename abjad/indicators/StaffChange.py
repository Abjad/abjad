from abjad import enums
from abjad.scheme import Scheme
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class StaffChange(AbjadValueObject):
    r"""
    Staff change.

    ..  container:: example

        Explicit staff change:

        >>> staff_group = abjad.StaffGroup()
        >>> staff_group.lilypond_type = 'PianoStaff'
        >>> rh_staff = abjad.Staff("c'8 d'8 e'8 f'8", name='RHStaff')
        >>> lh_staff = abjad.Staff("s2", name='LHStaff')
        >>> staff_group.extend([rh_staff, lh_staff])
        >>> staff_change = abjad.StaffChange(lh_staff)
        >>> abjad.attach(staff_change, rh_staff[2])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff_group)
            \new PianoStaff
            <<
                \context Staff = "RHStaff"
                {
                    c'8
                    d'8
                    \change Staff = LHStaff
                    e'8
                    f'8
                }
                \context Staff = "LHStaff"
                {
                    s2
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_staff',
        )

    _context = 'Staff'

    _format_leaf_children = False

    _format_slot = 'opening'

    _time_orientation: enums.HorizontalAlignment = enums.Right

    ### INITIALIZER ###

    def __init__(self, staff=None):
        from abjad.core.Staff import Staff
        if staff is not None:
            if not isinstance(staff, Staff):
                raise TypeError(f'must be staff: {staff!r}.')
        self._staff = staff

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""
        Gets string representation of staff change.

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

        """
        if self.staff is None:
            return r'\change Staff = ##f'
        value = Scheme.format_scheme_value(self.staff.name)
        return rf'\change Staff = {value}'

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Gets ``'Staff'``.

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

        """
        return self._context

    @property
    def staff(self):
        """
        Gets staff of staff change.

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

        Returns staff or none.
        """
        return self._staff

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on staff change.
        """
        pass
