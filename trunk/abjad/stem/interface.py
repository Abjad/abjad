from abjad.core.attributeformatter import _AttributeFormatter
from abjad.core.interface import _Interface
from abjad.core.spannerreceptor import _SpannerReceptor


class _StemInterface(_Interface, _AttributeFormatter, _SpannerReceptor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _AttributeFormatter.__init__(self, 'Stem')
      _SpannerReceptor.__init__(self, ['Stem'])
      self._tremolo = None

   @apply
   def tremolo( ):
      def fget(self):
         return self._tremolo
      def fset(self, expr):
         if expr == None:
            self._tremolo = None
         else:
            assert isinstance(expr, (int, long))
            assert not expr & (expr - 1)
            self._tremolo = expr
      return property(**locals( ))
