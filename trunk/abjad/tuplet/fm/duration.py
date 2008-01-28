from ... duration.rational import Rational
from .. duration import _TupletDurationInterface

class _FMTupletDurationInterface(_TupletDurationInterface):

   def __init__(self, _client, multiplier):
      _TupletDurationInterface.__init__(self, _client)
      self.multiplier = multiplier

   ### REPR ###

   def __repr__(self):
      return 'FMTupletDurationInterface(%s)' % str(self.multiplier)

   ### MANAGED ATTRIBUTES ###

   @apply
   def multiplier( ):
      def fget(self):
         return self._multiplier
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
            self._multiplier = rational
         else:
            raise ValueError('Tuplet rational %s must be positive.' %
               rational)
      return property(**locals( ))

   @property
   def _duration(self):
      if len(self._client) > 0:
         return self.multiplier * self.contents
      else:
         return Rational(0)
