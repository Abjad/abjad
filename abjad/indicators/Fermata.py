import dataclasses
import typing

from .. import bundle as _bundle
from .. import overrides as _overrides


@dataclasses.dataclass(unsafe_hash=True)
class Fermata:
    r"""
    Fermata.

    ..  container:: example

        A short fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata(command='shortfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
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

            >>> string = abjad.lilypond(score)
            >>> print(string)
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

            >>> string = abjad.lilypond(score)
            >>> print(string)
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

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \verylongfermata
                }
            >>

    ..  container:: example

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> fermata = abjad.Fermata()
        >>> abjad.tweak(fermata).color = "#blue"
        >>> abjad.attach(fermata, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            \fermata

    """

    command: str = "fermata"
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    _allowable_commands = (
        "fermata",
        "longfermata",
        "shortfermata",
        "verylongfermata",
    )

    context = "Score"

    _format_slot = "after"

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    #    ### SPECIAL METHODS ###
    #
    #    def __eq__(self, argument) -> bool:
    #        """
    #        Delegates to ``abjad.format.compare_objects()``.
    #        """
    #        return _format.compare_objects(self, argument)
    #
    #    def __hash__(self) -> int:
    #        """
    #        Hashes fermata.
    #        """
    #        return hash(self.__class__.__name__ + str(self))
    #
    #    def __repr__(self) -> str:
    #        """
    #        Gets interpreter representation.
    #        """
    #        return _format.get_repr(self)

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

        """
        return rf"\{self.command}"

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle

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


#    @property
#    def command(self) -> typing.Optional[str]:
#        """
#        Gets command of fermata.
#
#        ..  container:: example
#
#            Fermata:
#
#            >>> fermata = abjad.Fermata()
#            >>> fermata.command
#            'fermata'
#
#        ..  container:: example
#
#            Long fermata:
#
#            >>> fermata = abjad.Fermata('longfermata')
#            >>> fermata.command
#            'longfermata'
#
#        """
#        return self._command
#
#    @property
#    def tweaks(self) -> typing.Optional[_overrides.TweakInterface]:
#        r"""
#        Gets tweaks
#
#        """
#        return self._tweaks
