from abjad.tools.spannertools.GlissandoSpanner._GlissandoSpannerFormatInterface import _GlissandoSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class GlissandoSpanner(Spanner):
   '''Abjad glissando spanner.

   Return glissando spanner.
   '''

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _GlissandoSpannerFormatInterface(self)
