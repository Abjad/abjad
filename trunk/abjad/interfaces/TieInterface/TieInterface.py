from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor
from abjad.spanners import TieSpanner


class TieInterface(_Interface, _FormatContributor, _SpannerReceptor):
   '''Handle LilyPond Tie grob and Abjad Tie spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Tie grob.
      Receive Abjad Tie spanner.'''
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      _SpannerReceptor.__init__(self, (TieSpanner, ))
