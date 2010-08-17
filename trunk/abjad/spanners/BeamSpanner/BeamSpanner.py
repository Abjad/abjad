from abjad.spanners.BeamSpanner._BeamSpannerFormatInterface import _BeamSpannerFormatInterface
from abjad.spanners.Spanner import Spanner


class BeamSpanner(Spanner):

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _BeamSpannerFormatInterface(self)
