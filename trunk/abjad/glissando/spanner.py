from abjad.glissando.format import _GlissandoSpannerFormatInterface
from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Glissando(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Glissando', music)
      self._format = _GlissandoSpannerFormatInterface(self)
