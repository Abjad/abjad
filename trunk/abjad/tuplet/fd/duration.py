from abjad.duration.rational import Rational
from abjad.tuplet.duration import _TupletDurationInterface


class _FDTupletDurationInterface(_TupletDurationInterface):

   #def __init__(self, _client, duration):
   def __init__(self, _client, target):
      _TupletDurationInterface.__init__(self, _client)
      #self._duration = duration
      self.target = target

#   ### OVERLOADS ###
#
#   def __repr__(self):
#      #return 'FDTupletDurationInterface(%s)' % self._duration
#      return 'FDTupletDurationInterface(%s)' % self.target

   ### PUBLIC ATTRIBUTES ###

#   @apply
#   def _duration( ):
#      def fget(self):
#         return self._fixed
#      def fset(self, expr):
#         if isinstance(expr, (int, long)):
#            rational = Rational(expr)
#         elif isinstance(expr, tuple):
#            rational = Rational(*expr)
#         elif isinstance(expr, Rational):
#            rational = Rational(*expr.pair)
#         else:
#            raise ValueError('Can not set tuplet rational from %s.' % 
#               str(expr))
#         if rational > 0:
#            self._fixed = rational
#         else:
#            raise ValueError('Tuplet rational %s must be positive.' %
#               rational)
#      return property(**locals( ))

   @property
   def multiplied(self):
      return self.target

   @property
   def multiplier(self):
      if len(self._client) > 0:
         #return self._duration / self.contents
         return self.target / self.contents
      else:
         return None

   @apply
   def target( ):
      def fget(self):
         #return self._fixed
         return self._target
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
            #self._fixed = rational
            self._target = rational
         else:
            raise ValueError('Tuplet rational %s must be positive.' %
               rational)
      return property(**locals( ))
