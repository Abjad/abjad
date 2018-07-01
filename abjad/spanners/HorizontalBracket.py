import typing
from abjad.markups import Markup
from .Spanner import Spanner


class HorizontalBracket(Spanner):
    r"""
    Horizontal bracket.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')

        >>> spanner = abjad.HorizontalBracket()
        >>> abjad.tweak(spanner).staff_padding = 6
        >>> abjad.tweak(spanner).color = 'blue'
        >>> abjad.attach(spanner, voice[:])

        >>> spanner = abjad.HorizontalBracket()
        >>> abjad.tweak(spanner).staff_padding = 4
        >>> abjad.tweak(spanner).color = 'red'
        >>> abjad.attach(spanner, voice[:2])

        >>> spanner = abjad.HorizontalBracket()
        >>> abjad.tweak(spanner).staff_padding = 4
        >>> abjad.tweak(spanner).color = 'red'
        >>> abjad.attach(spanner, voice[2:])


        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            \with
            {
                \consists Horizontal_bracket_engraver
            }
            {
                c'4
                - \tweak color #blue
                - \tweak staff-padding #6
                \startGroup
                - \tweak color #red
                - \tweak staff-padding #4
                \startGroup
                d'4
                \stopGroup
                e'4
                - \tweak color #red
                - \tweak staff-padding #4
                \startGroup
                f'4
                \stopGroup
                \stopGroup
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_markup',
        )

    _start_command = r'\startGroup'

    _stop_command = r'\stopGroup'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        markup: Markup = None,
        ) -> None:
        Spanner.__init__(self)
        if markup is not None:
            assert isinstance(markup, Markup)
        self._markup = markup

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if leaf is self[0]:
            strings = self._tweaked_start_command_strings()
            bundle.after.spanner_starts.extend(strings)
        if leaf is self[-1]:
            string = self._stop_command_string()
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self) -> typing.Optional[Markup]:
        """
        Gets horizonal bracket markup.

        ..  container:: example

            Gets markup:

            >>> markup = abjad.Markup('3-1[012]').smaller()
            >>> spanner = abjad.HorizontalBracket(markup=markup)

            >>> spanner.markup
            Markup(contents=[MarkupCommand('smaller', '3-1[012]')])

        ..  container:: example

            Defaults to none:

            >>> spanner = abjad.HorizontalBracket()
            >>> spanner.markup is None
            True

        """
        return self._markup
