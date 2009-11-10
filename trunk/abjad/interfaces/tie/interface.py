from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.interfaces.spanner_receptor.receptor import _SpannerReceptor
from abjad.spanners import Tie


class TieInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond Tie grob and Abjad Tie spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Tie grob.
      Receive Abjad Tie spanner.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Tie')
      _SpannerReceptor.__init__(self, (Tie, ))
