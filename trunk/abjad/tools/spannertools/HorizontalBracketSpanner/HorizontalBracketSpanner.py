from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.HorizontalBracketSpanner._HorizontalBracketSpannerFormatInterface import _HorizontalBracketSpannerFormatInterface


class HorizontalBracketSpanner(Spanner):
    r'''.. versionadded:: 2.4

    Abjad horizontal bracket spanner::

        abjad> voice = Voice("c'4 d'4 e'4 f'4")
        abjad> voice.engraver_consists.add('Horizontal_bracket_engraver')

    ::

        abjad> horizontal_bracket_spanner = spannertools.HorizontalBracketSpanner(voice[:])

    ::

        abjad> horizontal_bracket_spanner
        HorizontalBracketSpanner(c'4, d'4, e'4, f'4)

    ::

        abjad> f(voice)
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

    def __init__(self, components = None):
        Spanner.__init__(self, components)
        self._format = _HorizontalBracketSpannerFormatInterface(self)
