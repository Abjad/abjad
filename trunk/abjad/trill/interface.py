from abjad.core.attributeformatter import _AttributeFormatter
from abjad.core.interface import _Interface
from abjad.core.spannerreceptor import _SpannerReceptor

#class _TrillInterface(_Interface):
class _TrillInterface(_Interface, _AttributeFormatter, _SpannerReceptor):

   def __init__(self, client):
      #_Interface.__init__(self, client, 'TrillSpanner', ['Trill'] )
      _Interface.__init__(self, client)
      _AttributeFormatter.__init__(self, 'TrillSpanner')
      _SpannerReceptor.__init__(self, ['Trill'])
      self._set = None
