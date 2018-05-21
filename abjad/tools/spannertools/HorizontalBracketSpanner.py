import typing
from abjad.tools.markuptools.Markup import Markup
from .Spanner import Spanner


class HorizontalBracketSpanner(Spanner):
    r"""
    Horizontal bracket spanner.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')

        >>> spanner = abjad.HorizontalBracketSpanner()
        >>> abjad.tweak(spanner).staff_padding = 6
        >>> abjad.tweak(spanner).color = 'blue'
        >>> abjad.attach(spanner, voice[:])

        >>> spanner = abjad.HorizontalBracketSpanner()
        >>> abjad.tweak(spanner).staff_padding = 4
        >>> abjad.tweak(spanner).color = 'red'
        >>> abjad.attach(spanner, voice[:2])

        >>> spanner = abjad.HorizontalBracketSpanner()
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
        leak: bool = None,
        markup: Markup = None,
        ) -> None:
        Spanner.__init__(self, leak=leak)
        if markup is not None:
            assert isinstance(markup, Markup)
        self._markup = markup

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if leaf is self[0]:
            strings = self.start_command()
            bundle.right.spanner_starts.extend(strings)
        if leaf is self[-1]:
            string = self.stop_command()
            bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def leak(self):
        r"""
        Is true when spanner leaks one leaf to the right.

        ..  container:: example

            Without leak:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> voice.consists_commands.append('Horizontal_bracket_engraver')
            >>> spanner = abjad.HorizontalBracketSpanner()
            >>> abjad.tweak(spanner).staff_padding = 4
            >>> abjad.attach(spanner, voice[:3])
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
                    - \tweak staff-padding #4
                    \startGroup
                    d'4
                    e'4
                    \stopGroup
                    f'4
                }

            With leak:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> voice.consists_commands.append('Horizontal_bracket_engraver')
            >>> spanner = abjad.HorizontalBracketSpanner(leak=True)
            >>> abjad.tweak(spanner).staff_padding = 4
            >>> abjad.attach(spanner, voice[:3])
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
                    - \tweak staff-padding #4
                    \startGroup
                    d'4
                    e'4
                    <> \stopGroup
                    f'4
                }

        """
        return super(HorizontalBracketSpanner, self).leak

    @property
    def markup(self) -> typing.Optional[Markup]:
        """
        Gets horizonal bracket spanner markup.

        ..  container:: example

            Gets markup:

            >>> markup = abjad.Markup('3-1[012]').smaller()
            >>> spanner = abjad.HorizontalBracketSpanner(markup=markup)

            >>> spanner.markup
            Markup(contents=[MarkupCommand('smaller', '3-1[012]')])

        ..  container:: example

            Defaults to none:

            >>> spanner = abjad.HorizontalBracketSpanner()
            >>> spanner.markup is None
            True

        """
        return self._markup

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.List[str]:
        r"""
        Gets start command.

        ..  container:: example

            >>> abjad.HorizontalBracketSpanner().start_command()
            ['\\startGroup']

        """
        return super(HorizontalBracketSpanner, self).start_command()

    def stop_command(self) -> typing.Optional[str]:
        r"""
        Gets stop command.

        ..  container:: example

            >>> abjad.HorizontalBracketSpanner().stop_command()
            '\\stopGroup'

            With leak:

            >>> abjad.HorizontalBracketSpanner(leak=True).stop_command()
            '<> \\stopGroup'

        """
        string = super(HorizontalBracketSpanner, self).stop_command()
        if self.leak:
            string = f'{self._empty_chord} {string}'
        return string
