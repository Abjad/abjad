from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.TextSpanner._TextSpannerFormatInterface import _TextSpannerFormatInterface


class TextSpanner(Spanner):
   r'''.. versionadded:: 1.1.2

   Handle LilyPond TextSpanner grob.

   Interface LilyPond ``\startTextSpan``, ``\stopTextSpan`` commands.

   Interface LilyPond ``\textSpannerUp``, ``\textSpannerDown`` commands. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> spanner = spannertools.TextSpanner(staff[:])
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
      Spanner.__init__(self, music)
      self._format = _TextSpannerFormatInterface(self)
