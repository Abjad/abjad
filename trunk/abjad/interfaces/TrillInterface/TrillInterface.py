from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor


class TrillInterface(_Interface, _FormatContributor, _SpannerReceptor):
   '''Handle LilyPond TrillSpanner grob and Abjad Trill spanner.'''

   def __init__(self, client):
      from abjad.tools.spannertools import TrillSpanner
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      _SpannerReceptor.__init__(self, (TrillSpanner, ))
