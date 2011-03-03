from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.TextSpanner._TextSpannerFormatInterface import _TextSpannerFormatInterface


class TextSpanner(Spanner):
   r'''.. versionadded:: 1.1.2

   Abjad text spanner::

      abjad> staff = Staff(macros.scale(4))

   ::

      abjad> spanner = spannertools.TextSpanner(staff[:])
      abjad> spanner.color = 'red'

   ::

      abjad> f(staff)
      \new Staff {
              \override TextSpanner #'color = #red
              c'8 \startTextSpan
              d'8
              e'8
              f'8 \stopTextSpan
              \revert TextSpanner #'color
      }

   Override LilyPond TextSpanner grob.

   Return text spanner.
   '''

   def __init__(self, components = None):
      Spanner.__init__(self, components)
      self._format = _TextSpannerFormatInterface(self)
