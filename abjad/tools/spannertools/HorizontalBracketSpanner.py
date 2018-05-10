import typing
from abjad.tools.markuptools.Markup import Markup
from .Spanner import Spanner


class HorizontalBracketSpanner(Spanner):
    r'''
    Horizontal bracket spanner.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')
        >>> spanner = abjad.HorizontalBracketSpanner()
        >>> abjad.attach(spanner, voice[:])
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
                \startGroup
                d'4
                e'4
                f'4
                \stopGroup
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_markup',
        )

    ### INITIALIZER ###

    def __init__(
        self,
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
            bundle.right.spanner_starts.append(r'\startGroup')
        if leaf is self[-1]:
            bundle.right.spanner_stops.append(r'\stopGroup')
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self) -> typing.Optional[Markup]:
        r'''
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

        '''
        return self._markup
