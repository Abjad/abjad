from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor
from abjad.spanners import TrillSpanner


class TrillInterface(_Interface, _FormatContributor, _SpannerReceptor):
   '''Handle LilyPond TrillSpanner grob and Abjad Trill spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond TrillSpanner grob.
      Receive Abjad Trill spanner.'''
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      _SpannerReceptor.__init__(self, (TrillSpanner, ))
