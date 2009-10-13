from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor
from abjad.spanners.trill import Trill


class TrillInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond TrillSpanner grob and Abjad Trill spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond TrillSpanner grob.
         Receive Abjad Trill spanner.'''
      #from abjad.trill import Trill
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TrillSpanner')
      _SpannerReceptor.__init__(self, (Trill, ))
