from abjad.spanners.Spanner.positionalhandler import _PositionalGrobHandlerSpanner
from abjad.spanners.TextSpanner.format import _TextSpannerFormatInterface


class TextSpanner(_PositionalGrobHandlerSpanner):
   r'''.. versionadded:: 1.1.2

   Handle LilyPond TextSpanner grob.

   Interface LilyPond ``\startTextSpan``, ``\stopTextSpan`` commands.

   Interface LilyPond ``\textSpannerUp``, ``\textSpannerDown`` commands. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> spanner = TextSpanner(staff[:])
      abjad> spanner.color = 'red'
      abjad> f(staff)
      \new Staff {
              \override TextSpanner #'color = #red
              c'8 \startTextSpan
              d'8
              e'8
              f'8 \stopTextSpan
              \revert TextSpanner #'color
      }
   '''

   def __init__(self, music = None):
      _PositionalGrobHandlerSpanner.__init__(self, 'TextSpanner', music)
      self._format = _TextSpannerFormatInterface(self)
      self.position = None

   ## PRIVATE ATTRIBUTES ##

   _positions = {'neutral':r'\textSpannerNeutral', 
      'up':r'\textSpannerUp', 'down':r'\textSpannerDown', None:None}
