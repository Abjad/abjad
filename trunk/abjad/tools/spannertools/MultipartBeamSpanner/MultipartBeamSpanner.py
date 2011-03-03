from abjad.tools.spannertools.MultipartBeamSpanner._MultipartBeamSpannerFormatInterface import \
   _MultipartBeamSpannerFormatInterface
from abjad.tools.spannertools.BeamSpanner import BeamSpanner


class MultipartBeamSpanner(BeamSpanner):
   '''.. versionadded:: 1.1.2

   Abjad multipart beam spanner.

   Beam spanner avoids rests and large-duration notes.

   Return multipart beam spanner.
   '''

   def __init__(self, components = None):
      BeamSpanner.__init__(self, components)
      self._format = _MultipartBeamSpannerFormatInterface(self)
