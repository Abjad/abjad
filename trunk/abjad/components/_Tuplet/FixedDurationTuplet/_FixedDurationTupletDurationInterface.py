from abjad.core import Rational
from abjad.components._Tuplet._TupletDurationInterface import _TupletDurationInterface


class _FixedDurationTupletDurationInterface(_TupletDurationInterface):

   def __init__(self, _client, target):
      _TupletDurationInterface.__init__(self, _client)
      self.target = target

   ### PUBLIC ATTRIBUTES ###

   @property
   def multiplied(self):
      return self.target

   @property
   def multiplier(self):
      if len(self._client) > 0:
         return self.target / self.contents
      else:
         return None

   @apply
   def target( ):
      def fget(self):
         return self._target
      def fset(self, expr):
         if isinstance(expr, (int, long)):
            rational = Rational(expr)
         elif isinstance(expr, tuple):
            rational = Rational(*expr)
         elif isinstance(expr, Rational):
            rational = Rational(expr)
         else:
            raise ValueError('Can not set tuplet rational from %s.' % 
               str(expr))
         if rational > 0:
            self._target = rational
         else:
            raise ValueError('Tuplet rational %s must be positive.' %
               rational)
      return property(**locals( ))
