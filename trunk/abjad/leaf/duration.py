from abjad.core.duration import _DurationInterface
from abjad.core.interface import _Interface
from abjad.exceptions.assignability import AssignabilityError
from abjad.helpers.binary import _binary
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.hasname import hasname
from abjad.helpers.is_assignable import _is_assignable
from abjad.rational.rational import Rational
#from math import log, floor, ceil
import math


class _LeafDurationInterface(_DurationInterface):

   def __init__(self, _client, duration):
      _DurationInterface.__init__(self, _client)
      self.multiplier = None
      #self.written = duration
      self.written = Rational(*_duration_token_unpack(duration))
#      self._numerator = self.written._numerator
#      self._denominator = self.written._denominator

#   ### OVERLOADS ###
#
#   ### TODO: suppress __repr__ for this private class;
#   ###       will only be possible to supress __repr__
#   ###       on the _DurationInterface parent class
#   ###       no longer inherits from Rational;
#   ###       until that time, supressing __repr__
#   ###       here will simply cause self to display
#   ###       as a Rational.
#
#   def __repr__(self):
#      if self.multiplier is not None:
#         return '_LeafDurationInterface(%s, %s)' % (
#            str(self.written), str(self.multiplier))
#      else:
#         return '_LeafDurationInterface(%s)' % str(self.written)

   ### PRIVATE ATTRIBUTES ###

#   def _assignable(self, q):
##      return (not q._d & (q._d - 1)) and \
##         (0 < q < 2) and \
##         (not '01' in _binary(q._n)) 
#      return (not q._d & (q._d - 1)) and \
#         (0 < q < 16) and \
#         (not '01' in _binary(q._n)) 

   @property
   def _dots(self):
      return sum([int(x) for x in list(_binary(self.written._n))]) - 1

   @property
   def _dotted(self):
#      return '%s%s' % (self._number, '.' * self._dots)
      durationNames = {0.5:r'\breve', 0.25:r'\longa', 0.125:r'\maxima'}
      number = self._number
      if number in durationNames:
         number = durationNames[number]
      return '%s%s' % (number, '.' * self._dots)

   @property
   def _duration(self):
      if self.multiplier is not None:
         return self.written * self.multiplier
      else:
         return self.written

   @property
   def _flags(self):
      return max(-int(math.floor(math.log(float(self.written._n) / \
         self.written._d, 2))) - 2, 0)

   @property
   def _number(self):
      #return 2 ** (int(math.log(self.written._d, 2)) - self._dots)
      return 2 ** int(math.ceil(math.log(1/self.written, 2)))

   @property
   def _product(self):
      if self.multiplier is not None:
         return '%s * %s' % (self._dotted, self.multiplier)
      else:
         return self._dotted

   ### PUBLIC ATTRIBUTES ###

   @property
   def multiplied(self):
      if self.written:
         if self.multiplier:
            return self.written * self.multiplier
         else:
            return Rational(*self.written.pair)
      else:
         return None

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
#            elif isinstance(expr, tuple):
#               rational = Rational(*expr)
            elif isinstance(expr, (int, long)):
               rational = Rational(expr)
            else:
               raise ValueError('can not set duration multiplier')
            assert rational >= 0
            self._multiplier = rational
      return property(**locals( ))

   @apply
   def preprolated( ):
      def fget(self):
         return self.multiplied
      return property(**locals( ))

   @apply
   def written( ):
      def fget(self):
         return self._written
      def fset(self, expr):
         if isinstance(expr, Rational):
            rational = expr
#         elif isinstance(expr, tuple):
#            rational = Rational(*expr)
         elif isinstance(expr, (int, long)):
            rational = Rational(expr)
         else:
            raise ValueError('can not set written duration.')
         #if not self._assignable(rational):
         #   raise ValueError('%s is not notehead-assignable.' % str(rational))
         if not _is_assignable(rational):
            raise AssignabilityError('%s' % str(rational))
         self._written = rational
      return property(**locals( ))

   ### PUBLIC METHODS ###
   
#   def rewrite(self, duration):
#      if self.written:
#         previous = self.written
#         self.written = duration
#         if self.multiplier:
#            multiplier = previous * self.multiplier / self.written
#         else:
#            multiplier = previous / self.written
#         if multiplier != 1:
#            self.multiplier = multiplier

   def rewrite(self, target):
      previous = self.multiplied
      #self.written = target
      self.written = Rational(*_duration_token_unpack(target))
      self.multiplier = None
      multiplier = previous / self.written
      if multiplier != 1:
         self.multiplier = multiplier
