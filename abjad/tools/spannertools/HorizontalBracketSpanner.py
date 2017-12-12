from .Spanner import Spanner


class HorizontalBracketSpanner(Spanner):
    r'''Horizontal bracket spanner.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> voice.consists_commands.append('Horizontal_bracket_engraver')
        >>> spanner = abjad.HorizontalBracketSpanner()
        >>> abjad.attach(spanner, voice[:])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice \with {
                \consists Horizontal_bracket_engraver
            } {
                c'4 \startGroup
                d'4
                e'4
                f'4 \stopGroup
            }

    Formats LilyPond ``\startGroup`` command on first leaf in spanner.

    Formats LilyPond ``\stopGroup`` command on last leaf in spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_markup',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        markup=None,
        ):
        import abjad
        Spanner.__init__(self, overrides=overrides)
        if markup is not None:
            markup = abjad.Markup(markup)
        self._markup = markup

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_first_leaf(leaf):
            bundle.right.spanner_starts.append(r'\startGroup')
        if self._is_my_last_leaf(leaf):
            bundle.right.spanner_stops.append(r'\stopGroup')
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self):
        r'''Gets horizonal bracket spanner markup.

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

        Set to markup or none.

        Returns markup or none.
        '''
        return self._markup
