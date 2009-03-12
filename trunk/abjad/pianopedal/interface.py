from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _PianoPedalInterface(_Interface, _SpannerReceptor):

   def __init__(self, client):
      from abjad.pianopedal.spanner import PianoPedal
      _Interface.__init__(self, client)
      #_SpannerReceptor.__init__(self, ['PianoPedal'])
      _SpannerReceptor.__init__(self, (PianoPedal, ))

