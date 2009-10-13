from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.spanners.spanner.receptor import _SpannerReceptor
from abjad.spanners.tie import Tie


class TieInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond Tie grob and Abjad Tie spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Tie grob.
         Receive Abjad Tie spanner.'''
      #from abjad.tie import Tie
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Tie')
      _SpannerReceptor.__init__(self, (Tie, ))
