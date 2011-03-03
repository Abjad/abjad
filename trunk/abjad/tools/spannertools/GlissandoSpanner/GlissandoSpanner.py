from abjad.tools.spannertools.GlissandoSpanner._GlissandoSpannerFormatInterface import _GlissandoSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class GlissandoSpanner(Spanner):
   '''Abjad glissando spanner.

   Return glissando spanner.
   '''

   def __init__(self, components = None):
      Spanner.__init__(self, components)
      self._format = _GlissandoSpannerFormatInterface(self)
