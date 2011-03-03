from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.PhrasingSlurSpanner._PhrasingSlurSpannerFormatInterface import _PhrasingSlurSpannerFormatInterface


class PhrasingSlurSpanner(Spanner):
   '''Abjad phrasing slur spanner.

   Return phrasing slur spanner.
   '''

   def __init__(self, components = None):
      Spanner.__init__(self, components)
      self._format = _PhrasingSlurSpannerFormatInterface(self)
