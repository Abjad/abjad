from abjad.spanners.BeamSpanner._BeamSpannerFormatInterface import _BeamSpannerFormatInterface
from abjad.spanners.Spanner._GrobHandlerSpanner import _GrobHandlerSpanner


class BeamSpanner(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Beam', music)
      self._format = _BeamSpannerFormatInterface(self)
