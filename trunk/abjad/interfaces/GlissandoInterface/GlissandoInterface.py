from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor


class GlissandoInterface(_Interface, _FormatContributor, _SpannerReceptor):
   '''Receive Abjad GlissandoSpanner.
   '''

   def __init__(self, _client):
      from abjad.tools.spannertools import GlissandoSpanner
      _Interface.__init__(self, _client)
      _FormatContributor.__init__(self)
      _SpannerReceptor.__init__(self, (GlissandoSpanner, ))
