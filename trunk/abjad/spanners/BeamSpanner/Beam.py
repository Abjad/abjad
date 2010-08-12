from abjad.spanners.Beam._BeamSpannerFormatInterface import _BeamSpannerFormatInterface
from abjad.spanners.Spanner._GrobHandlerSpanner import _GrobHandlerSpanner


class Beam(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Beam', music)
      self._format = _BeamSpannerFormatInterface(self)
