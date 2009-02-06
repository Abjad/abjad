from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.helpers.is_power_of_two import _is_power_of_two
from abjad.spanner.receptor import _SpannerReceptor


class _StemInterface(_Interface, _GrobHandler, _SpannerReceptor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Stem')
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
            assert _is_power_of_two(expr)
            self._tremolo = expr
      return property(**locals( ))
