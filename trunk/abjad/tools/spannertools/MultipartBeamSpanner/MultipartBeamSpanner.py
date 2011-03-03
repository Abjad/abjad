from abjad.tools.spannertools.MultipartBeamSpanner._MultipartBeamSpannerFormatInterface import \
   _MultipartBeamSpannerFormatInterface
from abjad.tools.spannertools.BeamSpanner import BeamSpanner


class MultipartBeamSpanner(BeamSpanner):
   r'''.. versionadded:: 1.1.2

   Abjad multipart beam spanner::

      abjad> staff = Staff("c'8 d'8 e'4 f'8 g'8 r4")

   ::

      abjad> spannertools.MultipartBeamSpanner(staff[:])
      MultipartBeamSpanner(c'8, d'8, e'4, f'8, g'8, r4)

   ::

      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
         e'4
         f'8 [
         g'8 ]
         r4
      }

   Avoid rests.

   Avoid large-duration notes.

   Return multipart beam spanner.
   '''

   def __init__(self, components = None):
      BeamSpanner.__init__(self, components)
      self._format = _MultipartBeamSpannerFormatInterface(self)
