from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.TextScriptSpanner._TextScriptSpannerFormatInterface import \
   _TextScriptSpannerFormatInterface


class TextScriptSpanner(Spanner):
   r'''.. versionadded:: 1.1.2

   Handle Lilypond TextScript grob.

   ::

      abjad> staff = Staff(macros.scale(4))
      abjad> spanner = spannertools.TextScriptSpanner(staff[:])
      abjad> spanner.color = 'red'
      abjad> markuptools.Markup(r'\italic { espressivo }', 'up')(staff[1])
      abjad> f(staff)
      \new Staff {
              \override TextScript #'color = #red
              c'8
              d'8 ^ \markup { \italic { espressivo } }
              e'8
              f'8
              \revert TextScript #'color
      }      
   '''

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _TextScriptSpannerFormatInterface(self)
