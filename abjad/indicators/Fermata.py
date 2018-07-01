import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class Fermata(AbjadValueObject):
    r"""
    Fermata.

    ..  container:: example

        A short fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata(command='shortfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \shortfermata
                }
            >>

    ..  container:: example

        A fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata()
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \fermata
                }
            >>

    ..  container:: example

        A long fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata('longfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \longfermata
                }
            >>

    ..  container:: example

        A very long fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata('verylongfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \verylongfermata
                }
            >>

    """

    ### CLASS VARIABLES ###

    _allowable_commands = (
        'fermata',
        'longfermata',
        'shortfermata',
        'verylongfermata',
        )

    __slots__ = (
        '_command',
        '_tweaks',
        )

    _context = 'Score'

    _format_slot = 'after'

    ### INITIALIZER ###

    def __init__(
        self,
        command: str = 'fermata',
        *,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        assert command in self._allowable_commands, repr(command)
        self._command = command
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""
        Gets string representation of fermata.

        ..  container:: example

            Fermata:

            >>> str(abjad.Fermata())
            '\\fermata'

        ..  container:: example

            Long fermata:

            >>> str(abjad.Fermata('longfermata'))
            '\\longfermata'

        Returns string.
        """
        return rf'\{self.command}'

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_commands() -> typing.Tuple[str, ...]:
        """
        Lists allowable commands:

        ..  container:: example

            All allowable commands:

            >>> commands = abjad.Fermata.list_allowable_commands()
            >>> for command in commands:
            ...     command
            'fermata'
            'longfermata'
            'shortfermata'
            'verylongfermata'

        """
        return Fermata._allowable_commands

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> typing.Optional[str]:
        """
        Gets command of fermata.

        ..  container:: example

            Fermata:

            >>> fermata = abjad.Fermata()
            >>> fermata.command
            'fermata'

        ..  container:: example

            Long fermata:

            >>> fermata = abjad.Fermata('longfermata')
            >>> fermata.command
            'longfermata'

        """
        return self._command

    @property
    def context(self) -> str:
        """
        Gets (historically conventional) context.

        ..  container:: example

            Fermata:

            >>> fermata = abjad.Fermata()
            >>> fermata.context
            'Score'

        ..  container:: example

            Long fermata:

            >>> fermata = abjad.Fermata('longfermata')
            >>> fermata.context
            'Score'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> fermata = abjad.Fermata()
            >>> abjad.tweak(fermata).color = 'blue'
            >>> abjad.attach(fermata, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                \fermata

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> fermata = abjad.Fermata(tweaks=[('color', 'blue')])
            >>> abjad.attach(fermata, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                \fermata

        """
        return self._tweaks
