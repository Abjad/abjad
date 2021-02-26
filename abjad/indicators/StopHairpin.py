import typing

from ..bundle import LilyPondFormatBundle
from ..storage import StorageFormatManager


class StopHairpin:
    r"""
    LilyPond ``\!`` command.

    ..  container:: example

        >>> abjad.StopHairpin()
        StopHairpin()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_leak",)

    _context = "Voice"

    # _parameter = 'DYNAMIC'

    # _persistent = True

    ### INITIALIZER ###

    def __init__(self, *, leak: bool = None) -> None:
        if leak is not None:
            leak = bool(leak)
        self._leak = leak

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = r"\!"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            # bundle.after.spanner_stops.append(string)
            bundle.after.articulations.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StopHairpin().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when stop slur leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> start_hairpin = abjad.StartHairpin('<')
            >>> abjad.tweak(start_hairpin).color = "#blue"
            >>> abjad.attach(start_hairpin, staff[0])
            >>> stop_hairpin = abjad.StopHairpin()
            >>> abjad.attach(stop_hairpin, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \<
                    d'4
                    e'4
                    \!
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> start_hairpin = abjad.StartHairpin('<')
            >>> abjad.tweak(start_hairpin).color = "#blue"
            >>> abjad.attach(start_hairpin, staff[0])
            >>> stop_hairpin = abjad.StopHairpin(leak=True)
            >>> abjad.attach(stop_hairpin, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \<
                    d'4
                    e'4
                    <> \!
                    r4
                }

        """
        return self._leak

    #    @property
    #    def parameter(self) -> str:
    #        """
    #        Returns ``'DYNAMIC'``.
    #
    #        ..  container:: example
    #
    #            >>> abjad.StopHairpin().parameter
    #            'DYNAMIC'
    #
    #        Class constant.
    #        """
    #        return self._parameter

    #    @property
    #    def persistent(self) -> bool:
    #        """
    #        Is true.
    #
    #        ..  container:: example
    #
    #            >>> abjad.StopHairpin().persistent
    #            True
    #
    #        Class constant.
    #        """
    #        return self._persistent

    @property
    def spanner_stop(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopHairpin().spanner_stop
            True

        """
        return True
