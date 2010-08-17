from abjad.tools.spannertools.GlissandoSpanner._GlissandoSpannerFormatInterface import _GlissandoSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class GlissandoSpanner(Spanner):
   '''Model glissando covering two or more notes.
   Handle LilyPond Glissando grob.'''

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _GlissandoSpannerFormatInterface(self)
