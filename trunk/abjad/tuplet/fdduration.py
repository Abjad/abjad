from .. duration.rational import Rational
from duration import _TupletDurationInterface

class _FDTupletDurationInterface(_TupletDurationInterface):

   def __init__(self, _client, duration):
      _TupletDurationInterface.__init__(self, _client)
      self._fixed = duration

   ### REPR ###

   def __repr__(self):
      return 'FDTupletDurationInterface( )'

   ### MANAGED ATTRIBUTES ###

   @apply
   def fixed( ):
      def fget(self):
         return self._fixed
      def fset(self, expr):
         if isinstance(expr, (int, long)):
            rational = Rational(expr)
         elif isinstance(expr, tuple):
            rational = Rational(*expr)
         elif isinstance(expr, Rational):
            rational = Rational(*expr.pair)
         else:
            raise ValueError('Can not set tuplet rational from %s.' % 
               str(expr))
         if rational > 0:
            self._fixed = rational
         else:
            raise ValueError('Tuplet rational %s must be positive.' %
               rational)
      return property(**locals( ))

   @property
   def resultant(self):
      return self.fixed

   @property
   def multiplier(self):
      if len(self._client) > 0:
         return self.fixed / self.composite
      else:
         return None
