from .. import enums
from ..bundle import LilyPondFormatBundle
from ..storage import StorageFormatManager


class StaffChange:
    r"""
    Staff change.

    ..  container:: example

        Explicit staff change:

        >>> staff_group = abjad.StaffGroup()
        >>> staff_group.lilypond_type = 'PianoStaff'
        >>> rh_staff = abjad.Staff("c'8 d'8 e'8 f'8", name='RHStaff')
        >>> lh_staff = abjad.Staff("s2", name='LHStaff')
        >>> staff_group.extend([rh_staff, lh_staff])
        >>> staff_change = abjad.StaffChange("LHStaff")
        >>> abjad.attach(staff_change, rh_staff[2])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
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

    __slots__ = ("_staff",)

    _context = "Staff"

    _format_leaf_children = False

    _format_slot = "opening"

    _time_orientation = enums.Right

    ### INITIALIZER ###

    def __init__(self, staff=None):
        if staff is not None:
            assert isinstance(staff, str), repr(staff)
        self._staff = staff

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

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
            >>> staff_change = abjad.StaffChange("LHStaff")
            >>> print(str(staff_change))
            \change Staff = LHStaff

        """
        if self.staff is None:
            return r"\change Staff = ##f"
        value = str(self.staff)
        return rf"\change Staff = {value}"

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
            >>> staff_change = abjad.StaffChange("LHStaff")
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
            >>> staff_change = abjad.StaffChange("LHStaff")
            >>> staff_change.staff
            'LHStaff'

        Returns staff or none.
        """
        return self._staff

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on staff change.
        """
        pass
