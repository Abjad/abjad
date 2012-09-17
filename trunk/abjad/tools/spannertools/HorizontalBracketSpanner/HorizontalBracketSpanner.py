from abjad.tools.spannertools.Spanner import Spanner


class HorizontalBracketSpanner(Spanner):
    r'''.. versionadded:: 2.4

    Abjad horizontal bracket spanner::

        >>> voice = Voice("c'4 d'4 e'4 f'4")
        >>> voice.engraver_consists.append('Horizontal_bracket_engraver')

    ::

        >>> horizontal_bracket_spanner = spannertools.HorizontalBracketSpanner(voice[:])

    ::

        >>> horizontal_bracket_spanner
        HorizontalBracketSpanner(c'4, d'4, e'4, f'4)

    ::

        >>> f(voice)
        \new Voice \with {
            \consists Horizontal_bracket_engraver
        } {
            c'4 \startGroup
            d'4
            e'4
            f'4 \stopGroup
        }

    Return horizontal bracket spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None):
        Spanner.__init__(self, components)

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\startGroup')
        if self._is_my_last_leaf(leaf):
            result.append(r'\stopGroup')
        return result
