from .. core.duration import _DurationInterface
from .. core.interface import _Interface
from .. helpers.binary import binary
from .. helpers.hasname import hasname
from .. duration.rational import Rational
from math import log, floor

class LeafDurationInterface(_DurationInterface):

   def __init__(self, _client, duration):
      _DurationInterface.__init__(self, _client)
      self.multiplier = None
      self.written = duration

   ### REPR ###

   def __repr__(self):
      if self.multiplier is not None:
         return 'DurationInterface(%s, %s)' % (
            str(self.written), str(self.multiplier))
      else:
         return 'DurationInterface(%s)' % str(self.written)

   ### READ-ONLY ATTRIBUTES ###

   @property
   #def _multiplied(self):
   def _duration(self):
      if self.multiplier is not None:
         return self.written * self.multiplier
      else:
         return self.written

#   @property
#   def absolute(self):
#      result = self.written * self.prolation
#      if self.multiplier is not None:
#         result *= self.multiplier
#      return result

   ### BOUND METHODS ###
   
   def rewrite(self, duration):
      if self.written:
         previous = self.written
         self.written = duration
         if self.multiplier:
            multiplier = previous * self.multiplier / self.written
         else:
            multiplier = previous / self.written
         if multiplier != 1:
            self.multiplier = multiplier

   ### MANAGED ATTRIBUTES ###

   @apply
   def multiplier( ):
      def fget(self):
         return self._multiplier
      def fset(self, expr):
         if expr is None:
            self._multiplier = None
         else:
            if isinstance(expr, Rational):
               rational = expr
            elif isinstance(expr, tuple):
               rational = Rational(*expr)
            elif isinstance(expr, (int, long)):
               rational = Rational(expr)
            else:
               raise ValueError('can not set duration multiplier')
            assert rational > 0
            self._multiplier = rational
      return property(**locals( ))

   @apply
   def written( ):
      def fget(self):
         return self._written
      def fset(self, expr):
         if isinstance(expr, Rational):
            rational = expr
         elif isinstance(expr, tuple):
            rational = Rational(*expr)
         elif isinstance(expr, (int, long)):
            rational = Rational(expr)
         else:
            raise ValueError('can not set written duration.')
         if not self._assignable(rational):
            raise ValueError('%s is not notehead-assignable.' % str(rational))
         self._written = rational
      return property(**locals( ))

   ### PREDICATES ###
         
   def _assignable(self, q):
      return (not q._d & (q._d - 1)) and \
         (0 < q < 2) and \
         (not '01' in binary(q._n)) 

   ### PROPERTIES ###

   @property
   def _number(self):
      return 2 ** (int(log(self.written._d, 2)) - self._dots)

   @property
   def _dots(self):
      return sum([int(x) for x in list(binary(self.written._n))]) - 1

   @property
   def _flags(self):
      return max(-int(floor(log(float(self.written._n) / \
         self.written._d, 2))) - 2, 0)

   ### FORMATTING ###

   @property
   def _dotted(self):
      return '%s%s' % (self._number, '.' * self._dots)

   @property
   def _product(self):
      if self.multiplier is not None:
         return '%s * %s' % (self._dotted, self.multiplier)
      else:
         return self._dotted
