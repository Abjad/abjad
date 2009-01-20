#from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


#class _PianoPedalInterface(_Interface, _GrobHandler, _SpannerReceptor):
class _PianoPedalInterface(_Interface, _SpannerReceptor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      #_GrobHandler.__init__(self, 'SustainPedal')
      _SpannerReceptor.__init__(self, ['PianoPedal'])

