from abjad.tools.spannertools.BeamSpanner._BeamSpannerFormatInterface import _BeamSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class BeamSpanner(Spanner):

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _BeamSpannerFormatInterface(self)
