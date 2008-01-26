from .. core.interface import _Interface

class StemInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Stem', ['Stem'])
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
