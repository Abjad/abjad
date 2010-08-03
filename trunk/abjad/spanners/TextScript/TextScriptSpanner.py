from abjad.spanners.Spanner.grobhandler import _GrobHandlerSpanner
from abjad.spanners.TextScript.format import _TextScriptSpannerFormatInterface


class TextScriptSpanner(_GrobHandlerSpanner):
   r'''.. versionadded:: 1.1.2

   Handle Lilypond TextScript grob.

   ::

      abjad> staff = Staff(macros.scale(4))
      abjad> spanner = TextScriptSpanner(staff[:])
      abjad> spanner.color = 'red'
      abjad> staff[1].markup.up.append(r'\italic { espressivo }')
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
      _GrobHandlerSpanner.__init__(self, 'TextScript', music)
      self._format = _TextScriptSpannerFormatInterface(self)
