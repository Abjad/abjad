from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _SlurInterface(_Interface, _GrobHandler, _SpannerReceptor):

   def __init__(self, client):
      from abjad.slur.spanner import Slur
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Slur')
      _SpannerReceptor.__init__(self, (Slur, ))
      self._counts = (None, None)

   ### PUBLIC ATTRIBUTES ###

   @property
   def closing(self):
      return self.spanned and ')' in self.spanner._right(self._client)

   @property
   def opening(self):
      return self.spanned and '(' in self.spanner._right(self._client)
