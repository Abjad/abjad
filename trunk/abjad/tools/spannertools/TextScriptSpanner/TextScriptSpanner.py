from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.TextScriptSpanner._TextScriptSpannerFormatInterface import _TextScriptSpannerFormatInterface


class TextScriptSpanner(Spanner):
    r'''.. versionadded:: 2.0

    Abjad text script spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> spanner = spannertools.TextScriptSpanner(staff[:])
        abjad> spanner.override.text_script.color = 'red'
        abjad> markuptools.Markup(r'\italic { espressivo }', 'up')(staff[1])
        Markup('\\italic { espressivo }', '^')

    ::

        abjad> f(staff)
        \new Staff {
            \override TextScript #'color = #red
            c'8
            d'8 ^ \markup { \italic { espressivo } }
            e'8
            f'8
            \revert TextScript #'color
        }

    Override LilyPond TextScript grob.

    Return text script spanner.
    '''

    def __init__(self, components = None):
        Spanner.__init__(self, components)
        self._format = _TextScriptSpannerFormatInterface(self)
