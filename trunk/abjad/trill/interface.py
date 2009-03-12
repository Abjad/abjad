from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _TrillInterface(_Interface, _GrobHandler, _SpannerReceptor):

   def __init__(self, client):
      from abjad.trill.spanner import Trill
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TrillSpanner')
      #_SpannerReceptor.__init__(self, ['Trill'])
      _SpannerReceptor.__init__(self, (Trill, ))
      self._set = None
