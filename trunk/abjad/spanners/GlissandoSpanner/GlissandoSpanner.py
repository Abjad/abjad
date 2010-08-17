from abjad.spanners.GlissandoSpanner._GlissandoSpannerFormatInterface import _GlissandoSpannerFormatInterface
from abjad.spanners.Spanner import Spanner


class GlissandoSpanner(Spanner):
   '''Model glissando covering two or more notes.
   Handle LilyPond Glissando grob.'''

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _GlissandoSpannerFormatInterface(self)
