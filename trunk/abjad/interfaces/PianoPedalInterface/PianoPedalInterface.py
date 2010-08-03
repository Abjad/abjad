from abjad.interfaces._Interface import _Interface
from abjad.spanners import PianoPedal
from abjad.interfaces._SpannerReceptor import _SpannerReceptor


class PianoPedalInterface(_Interface, _SpannerReceptor):
   '''Handle LilyPond PianoPedal grob.
      Receive Abjad PianoPedal spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond PianoPedal grob.
         Receive Abjad PianoPedal spanner.'''
      _Interface.__init__(self, client)
      _SpannerReceptor.__init__(self, (PianoPedal, ))

