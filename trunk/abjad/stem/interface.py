from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.helpers.is_power_of_two import _is_power_of_two

 
class _StemInterface(_Interface, _GrobHandler):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Stem')
      self._tremolo = None
   
   ## PUBLIC ATTRIBUTES ##

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
