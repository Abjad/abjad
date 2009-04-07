from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _TieInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond Tie grob and Abjad Tie spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Tie grob.
         Receive Abjad Tie spanner.'''
      from abjad.tie.spanner import Tie
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Tie')
      _SpannerReceptor.__init__(self, (Tie, ))
