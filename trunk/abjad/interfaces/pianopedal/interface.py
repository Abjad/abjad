from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class PianoPedalInterface(_Interface, _SpannerReceptor):
   '''Handle LilyPond PianoPedal grob.
      Receive Abjad PianoPedal spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond PianoPedal grob.
         Receive Abjad PianoPedal spanner.'''
      from abjad.pianopedal import PianoPedal
      _Interface.__init__(self, client)
      _SpannerReceptor.__init__(self, (PianoPedal, ))

