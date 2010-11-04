from abjad.tools.spannertools.MultipartBeamSpanner._MultipartBeamSpannerFormatInterface import \
   _MultipartBeamSpannerFormatInterface
from abjad.tools.spannertools.BeamSpanner import BeamSpanner


class MultipartBeamSpanner(BeamSpanner):
   '''.. versionadded:: 1.1.2

   Beam spanner that avoids rests and large-duration notes.
   '''

   def __init__(self, music = None):
      BeamSpanner.__init__(self, music)
      self._format = _MultipartBeamSpannerFormatInterface(self)
